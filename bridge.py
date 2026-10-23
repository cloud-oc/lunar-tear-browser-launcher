import asyncio
import json
import pathlib
import struct
import subprocess
import time
import argparse
from aiohttp import web, WSMsgType
from app_config import ROOT, PACKAGE, load_config, asset_status
from platform_support import HIDDEN
from android_device import resolve_device, validate_serial

CONFIG = None
ADB = SERIAL = PORT = None
active = asyncio.Lock()

async def adb(*args):
    p = await asyncio.create_subprocess_exec(ADB, '-s', SERIAL, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, creationflags=HIDDEN)
    out, err = await p.communicate()
    if p.returncode:
        raise RuntimeError(err.decode(errors='replace'))
    return out

@web.middleware
async def local_only(request, handler):
    if request.host not in {f'127.0.0.1:{PORT}', f'localhost:{PORT}'}:
        raise web.HTTPForbidden()
    origin = request.headers.get('Origin')
    if request.path == '/stream' and not origin:
        raise web.HTTPForbidden(text='Browser Origin required')
    if origin and origin not in {f'http://127.0.0.1:{PORT}', f'http://localhost:{PORT}'}:
        raise web.HTTPForbidden()
    return await handler(request)

async def index(request):
    return web.FileResponse(ROOT / 'browser.html')

async def status(request):
    return web.json_response(asset_status(CONFIG))

async def stream(request):
    if active.locked():
        raise web.HTTPConflict(text='请先关闭另一个串流页面。')
    ws = web.WebSocketResponse(max_msg_size=4096, heartbeat=20)
    async with active:
        await ws.prepare(request)
        process = None
        writers = []
        tasks = []
        log = None
        try:
            await adb('push', CONFIG['scrcpy_server'], '/data/local/tmp/lunar-scrcpy.jar')
            stream_port = CONFIG['ports']['stream']
            scid = '0'+format(stream_port, '07x')
            await adb('forward', f'tcp:{stream_port}', f'localabstract:scrcpy_{scid}')
            log = (pathlib.Path(CONFIG['_runtime'])/'scrcpy.log').open('ab')
            video_config = CONFIG['video']
            process = await asyncio.create_subprocess_exec(ADB, '-s', SERIAL, 'shell', 'CLASSPATH=/data/local/tmp/lunar-scrcpy.jar', 'app_process', '/', 'com.genymobile.scrcpy.Server', '3.3.4', f'scid={scid}', 'tunnel_forward=true', 'send_device_meta=false', 'video_codec=h264', 'audio_codec=raw', f"audio={str(CONFIG['audio']).lower()}", 'control=true', f"max_size={video_config['max_size']}", f"max_fps={video_config['max_fps']}", f"video_bit_rate={video_config['bit_rate']}", 'clipboard_autosync=false', stdout=log, stderr=log, creationflags=HIDDEN)
            video = None
            for _ in range(30):
                try:
                    reader, writer = await asyncio.open_connection('127.0.0.1', stream_port)
                    await asyncio.wait_for(reader.readexactly(1), 2)
                    video = reader; writers.append(writer); break
                except (OSError, asyncio.IncompleteReadError, asyncio.TimeoutError):
                    if 'writer' in locals(): writer.close()
                    await asyncio.sleep(.2)
            if video is None: raise RuntimeError('无法启动模拟器画面串流')
            audio = None
            if CONFIG['audio']:
                audio, aw = await asyncio.open_connection('127.0.0.1', stream_port); writers.append(aw)
            control, cw = await asyncio.open_connection('127.0.0.1', stream_port); writers.append(cw)
            vh = await asyncio.wait_for(video.readexactly(12), 15)
            codec, width, height = struct.unpack('>III', vh)
            await ws.send_json({'type':'video', 'width':width, 'height':height})

            async def packets(reader, kind):
                if kind == b'A':
                    header = await reader.readexactly(4)
                    if int.from_bytes(header, 'big') in (0,1):
                        await ws.send_json({'type':'notice','text':'此模拟器暂时无法转发声音。'})
                        return
                while True:
                    header = await reader.readexactly(12)
                    size = int.from_bytes(header[8:12], 'big')
                    if size > 16*1024*1024: raise RuntimeError('Invalid frame')
                    await ws.send_bytes(kind + header + await reader.readexactly(size))

            async def monitored_packets(reader, kind):
                try: await packets(reader,kind)
                except (asyncio.IncompleteReadError, ConnectionError, RuntimeError) as exc:
                    print('Stream ended:', repr(exc), flush=True)
                    await ws.close()
            tasks = [asyncio.create_task(monitored_packets(video,b'V'))]
            if audio is not None: tasks.append(asyncio.create_task(monitored_packets(audio,b'A')))
            async for msg in ws:
                if msg.type != WSMsgType.TEXT: continue
                d = json.loads(msg.data)
                if d.get('type') == 'touch':
                    action = int(d['action'])
                    if action not in (0,1,2): continue
                    w,h = int(d['width']),int(d['height'])
                    if not 0<w<8192 or not 0<h<8192: continue
                    x,y = max(0,min(w-1,int(d['x']))),max(0,min(h-1,int(d['y'])))
                    cw.write(struct.pack('>BBQiiHHHII',2,action,0,x,y,w,h,0 if action==1 else 65535,0,0))
                    await cw.drain()
                elif d.get('type') == 'key' and int(d.get('key',0)) in (3,4,24,25,26):
                    for action in (0,1): cw.write(struct.pack('>BBIII',0,action,int(d['key']),0,0))
                    await cw.drain()
                elif d.get('type') == 'launch':
                    if not asset_status(CONFIG)['ready']:
                        await ws.send_json({'type':'error','text':'遊戲資源尚未就緒，請按 README 完成準備。'})
                        continue
                    await adb('shell','monkey','-p',PACKAGE,'-c','android.intent.category.LAUNCHER','1')
        except Exception as e:
            print('Stream:',repr(e),flush=True)
            if not ws.closed: await ws.send_json({'type':'error','text':str(e)})
        finally:
            for t in tasks:t.cancel()
            await asyncio.gather(*tasks,return_exceptions=True)
            for w in writers:w.close()
            if process and process.returncode is None:
                process.terminate()
                await process.wait()
            if log:log.close()
            try: await adb('forward','--remove',f"tcp:{CONFIG['ports']['stream']}")
            except Exception: pass
            await ws.close()
    return ws

def create_app(config):
    global CONFIG, ADB, SERIAL, PORT, active
    CONFIG = config
    ADB, SERIAL, PORT = config['adb'], config['serial'], config['ports']['web']
    active = asyncio.Lock()
    pathlib.Path(config['_runtime']).mkdir(parents=True, exist_ok=True)
    app=web.Application(middlewares=[local_only])
    app.add_routes([web.get('/',index),web.get('/status',status),web.get('/stream',stream)])
    return app

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',default=str(ROOT/'config.json'))
    parser.add_argument('--serial',help='Resolved ADB device selected by the launcher')
    args=parser.parse_args()
    cfg = load_config(args.config)
    cfg['serial']=validate_serial(args.serial) if args.serial else resolve_device(cfg)
    web.run_app(create_app(cfg),host='127.0.0.1',port=cfg['ports']['web'])
