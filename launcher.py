"""Local-only Windows launcher. No game files are downloaded by this project."""
import argparse
from contextlib import closing
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import sqlite3
import subprocess
import sys
import time
import urllib.request
import webbrowser
import zipfile

import psutil
from app_config import ROOT, PACKAGE, load_config, asset_status

HIDDEN = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
TOOLS = {
    'scrcpy': ('https://github.com/Genymobile/scrcpy/releases/download/v3.3.4/scrcpy-server-v3.3.4',
               '8588238c9a5a00aa542906b6ec7e6d5541d9ffb9b5d0f6e1bc0e365e2303079e'),
    'server': ('https://github.com/Walter-Sparrow/lunar-tear/releases/download/v1.0.2/lunar-tear-server-v1.0.2-windows-amd64.zip',
               'd8f6330a8f3a8788a89ba8ecfc01a5ff40ab566a9c46d9ff6fd0929503dd5f0a')}

def run(args, **kw):
    return subprocess.run([str(a) for a in args], check=True, creationflags=HIDDEN, **kw)

def adb(c, *args):
    return run([c['adb'], '-s', c['serial'], *args], capture_output=True, text=True, timeout=120).stdout

def download(url, destination, digest):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        if hashlib.sha256(destination.read_bytes()).hexdigest() == digest: return
        raise RuntimeError('Existing tool has unexpected hash: '+str(destination))
    tmp = destination.with_suffix(destination.suffix+'.part')
    print('Downloading', url, flush=True)
    with urllib.request.urlopen(url, timeout=60) as response, tmp.open('wb') as out:
        shutil.copyfileobj(response, out)
    if hashlib.sha256(tmp.read_bytes()).hexdigest() != digest:
        raise RuntimeError('SHA256 mismatch: '+str(tmp))
    tmp.replace(destination)

def fetch_tools(c):
    download(*[TOOLS['scrcpy'][0], c['scrcpy_server'], TOOLS['scrcpy'][1]])
    server = Path(c['server_dir'])
    if (server/'bin/dev.exe').is_file():
        print('Using existing server directory; version must be v1.0.2.')
        return
    if server.exists() and any(server.iterdir()):
        raise RuntimeError('Refusing to overwrite a nonempty server directory')
    archive = Path(c['_runtime'])/'downloads/server-v1.0.2.zip'
    download(TOOLS['server'][0], archive, TOOLS['server'][1])
    with zipfile.ZipFile(archive) as z:
        prefix = 'lunar-tear-server-v1.0.2-windows-amd64/'
        for item in z.infolist():
            if not item.filename.startswith(prefix): raise RuntimeError('Unexpected ZIP root')
            rel = Path(item.filename[len(prefix):])
            target = (server/rel).resolve()
            if not target.is_relative_to(server.resolve()): raise RuntimeError('Unsafe ZIP path')
            if item.is_dir(): target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with z.open(item) as src, target.open('wb') as out: shutil.copyfileobj(src, out)
    print('Pinned upstream tools ready.')

def init_db(c):
    """Only create a new v1.0.2 DB; never migrate or replace an existing save."""
    target = Path(c['server_dir'])/'db/game.db'
    if target.exists():
        print('Existing database preserved:', target)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_suffix('.initializing')
    if temp.exists(): raise RuntimeError('Previous initialization incomplete: '+str(temp))
    with closing(sqlite3.connect(temp)) as db:
        db.execute('CREATE TABLE goose_db_version (id INTEGER PRIMARY KEY AUTOINCREMENT, version_id INTEGER NOT NULL, is_applied INTEGER NOT NULL, tstamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        db.execute('INSERT INTO goose_db_version(version_id,is_applied) VALUES (0,1)')
        db.commit()
        for f in sorted((ROOT/'vendor/migrations').glob('*.sql')):
            sql = f.read_text(encoding='utf-8').split('-- +goose Up',1)[1].split('-- +goose Down',1)[0]
            version = int(f.name.split('_')[0])
            db.executescript('BEGIN;\n'+sql+f'\nINSERT INTO goose_db_version(version_id,is_applied) VALUES ({version},1);\nCOMMIT;')
        if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok': raise RuntimeError('Database integrity check failed')
    # Windows rename does not overwrite an existing destination.
    temp.rename(target)
    print('New database initialized.')

def import_assets(c):
    archive = Path(c['asset_archive'])
    if not c['asset_archive'] or not archive.is_file(): raise RuntimeError('Set asset_archive to your local Android .7z archive')
    if not Path(c['seven_zip']).is_file(): raise RuntimeError('Set seven_zip to 7z.exe')
    if c.get('asset_sha1'):
        h = hashlib.sha1()
        with archive.open('rb') as f:
            for block in iter(lambda:f.read(8*1024*1024),b''): h.update(block)
        if h.hexdigest().lower() != c['asset_sha1'].lower(): raise RuntimeError('Asset SHA1 mismatch')
    listing = run([c['seven_zip'],'l','-slt','-sccUTF-8',archive],capture_output=True,encoding='utf-8').stdout.split('----------',1)[1]
    from pathlib import PureWindowsPath
    for line in listing.splitlines():
        if line.startswith(('Symbolic Link = ', 'Hard Link = ')):
            raise RuntimeError('Archive links are not supported')
        if line.startswith('Path = '):
            p = PureWindowsPath(line[7:])
            if p.is_absolute() or p.drive or ':' in str(p) or '..' in p.parts or not p.parts or p.parts[0] != 'revisions':
                raise RuntimeError('Unexpected asset path: '+str(p))
    root = Path(c['server_dir'])/'assets'
    if (root/'revisions').exists(): raise RuntimeError('Existing revisions preserved; import into a fresh server directory')
    run([c['seven_zip'],'x',archive,'-o'+str(root),'-y','-bsp0'])
    print('Android archive extracted. Patched master data must also be supplied in assets/release/.')

def doctor(c):
    failed = []
    for label, path in [('ADB',c['adb']),('scrcpy',c['scrcpy_server']),
                        ('server',str(Path(c['server_dir'])/'bin/dev.exe')),
                        ('database',str(Path(c['server_dir'])/'db/game.db'))]:
        ok = Path(path).is_file()
        print(('OK   ' if ok else 'FAIL ')+label+': '+path)
        if not ok: failed.append(label)
    status = asset_status(c)
    print(('OK   ' if status['ready'] else 'WAIT ')+'assets: '+status['message'])
    print('APK must target 127.0.0.1 ports:', {k:c['ports'][k] for k in ('grpc','cdn','auth')})
    return failed

def listener(port):
    matches = [x for x in psutil.net_connections(kind='tcp')
               if x.status == psutil.CONN_LISTEN and x.laddr.port == port]
    if not matches: return None
    if len({x.pid for x in matches}) != 1 or any(x.laddr.ip != '127.0.0.1' for x in matches):
        raise RuntimeError(f'Port {port} has a non-local or ambiguous listener')
    return psutil.Process(matches[0].pid)

def process_identity(p):
    return {'pid':p.pid, 'created':p.create_time(), 'exe':p.exe()}

def owned_process(entry):
    try:
        p = psutil.Process(entry['pid'])
        if abs(p.create_time()-entry['created']) < .01 and os.path.normcase(p.exe()) == os.path.normcase(entry['exe']): return p
    except (psutil.Error, KeyError): pass
    return None

def stop(c):
    path = Path(c['_runtime'])/'processes.json'
    if not path.exists(): print('No launcher-owned processes.'); return
    stopped_bridge = False
    for entry in json.loads(path.read_text()):
        p = owned_process(entry)
        if not p: continue
        if str(ROOT/'bridge.py') in p.cmdline() and c['_path'] in p.cmdline(): stopped_bridge = True
        family = p.children(recursive=True)
        for child in reversed(family):
            try: child.terminate()
            except psutil.NoSuchProcess: pass
        try: p.terminate()
        except psutil.NoSuchProcess: pass
        psutil.wait_procs(family+[p], timeout=5)
    if stopped_bridge:
        port = c['ports']['stream']
        expected = [c['serial'], f'tcp:{port}', f'localabstract:scrcpy_{port:08x}']
        forwards = adb(c,'forward','--list')
        if any(line.split() == expected for line in forwards.splitlines()):
            adb(c,'forward','--remove',f'tcp:{port}')
    path.unlink()
    print('Launcher-owned services stopped. Emulator and pre-existing services left running.')

def start(c, open_browser=True):
    if os.name != 'nt': raise RuntimeError('Runtime is supported on Windows only')
    if doctor(c): raise RuntimeError('Resolve FAIL items first: setup / fetch-tools / init-db')
    runtime = Path(c['_runtime']); runtime.mkdir(parents=True, exist_ok=True)
    state = runtime/'processes.json'
    entries = json.loads(state.read_text()) if state.exists() else []
    entries = [e for e in entries if owned_process(e)]
    def spawn(args, cwd, name):
        with (runtime/(name+'.log')).open('ab') as log:
            p = subprocess.Popen([str(a) for a in args],cwd=cwd,stdout=log,stderr=subprocess.STDOUT,creationflags=HIDDEN)
        entries.append(process_identity(psutil.Process(p.pid)))
        state.write_text(json.dumps(entries))
        return p
    def wait_port(port, proc):
        for _ in range(60):
            if proc.poll() is not None: raise RuntimeError('Service exited; inspect runtime logs')
            if listener(port): return
            time.sleep(.5)
        raise RuntimeError('Service startup timed out; inspect runtime logs')

    # Check all ports before changing the emulator or starting services.
    server = Path(c['server_dir'])
    present = []
    for name, exe in [('grpc','lunar-tear.exe'),('cdn','octo-cdn.exe'),('auth','auth-server.exe')]:
        p = listener(c['ports'][name]); present.append(bool(p))
        if p and Path(p.exe()).resolve() != (server/'bin'/exe).resolve():
            raise RuntimeError(f'{name} port is occupied by a different program')
    if any(present) and not all(present): raise RuntimeError('Partial server already running; resolve it before start')
    web = listener(c['ports']['web'])
    if web:
        args = web.cmdline()
        if str(ROOT/'bridge.py') not in args or c['_path'] not in args:
            raise RuntimeError('Web port is occupied by another configuration/program')
    if not web and listener(c['ports']['stream']): raise RuntimeError('Stream port is already occupied')
    if c['emulator_manager']:
        run([c['emulator_manager'],'control','--vmindex',str(c['emulator_index']),'launch'],capture_output=True,timeout=60)
    for _ in range(60):
        run([c['adb'],'connect',c['serial']],capture_output=True,timeout=10)
        try:
            if adb(c,'get-state').strip() == 'device' and adb(c,'shell','getprop','sys.boot_completed').strip() == '1': break
        except subprocess.CalledProcessError: pass
        time.sleep(2)
    else: raise RuntimeError('Emulator did not finish booting')
    for name in ('grpc','cdn','auth'):
        port = c['ports'][name]
        adb(c,'reverse',f'tcp:{port}',f'tcp:{port}')
    if not all(present):
        # Consistent SQLite snapshot before each launcher-created server start.
        backups = runtime/'backups'; backups.mkdir(exist_ok=True)
        with closing(sqlite3.connect(server/'db/game.db')) as src, closing(sqlite3.connect(backups/(time.strftime('%Y%m%d-%H%M%S')+'.db'))) as dst: src.backup(dst)
        ports = c['ports']; args = [server/'bin/dev.exe','--no-color']
        for name in ('grpc','cdn','auth'): args += ['--'+name+'.listen',f"127.0.0.1:{ports[name]}"]
        for name in ('grpc','cdn'): args += ['--'+name+'.public-addr',f"127.0.0.1:{ports[name]}"]
        args += ['--grpc.octo-url',f"http://127.0.0.1:{ports['cdn']}",'--grpc.auth-url',f"http://127.0.0.1:{ports['auth']}"]
        proc = spawn(args,server,'server')
        for name in ('grpc','cdn','auth'): wait_port(ports[name],proc)
    if not web:
        proc = spawn([sys.executable,ROOT/'bridge.py','--config',c['_path']],ROOT,'bridge')
        wait_port(c['ports']['web'],proc)
    url = f"http://127.0.0.1:{c['ports']['web']}"
    print('Browser ready:',url)
    if open_browser: webbrowser.open(url)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',default=str(ROOT/'config.json'))
    parser.add_argument('--no-browser',action='store_true')
    parser.add_argument('command',choices=['init','fetch-tools','init-db','import-assets','install-apk','doctor','start','stop'])
    args = parser.parse_args()
    if args.command == 'init':
        path = Path(args.config)
        if path.exists(): print('Existing config preserved.')
        else: shutil.copyfile(ROOT/'config.example.json',path); print('Edit',path)
        return
    c = load_config(args.config)
    if args.command == 'start': start(c,not args.no_browser)
    elif args.command == 'stop': stop(c)
    elif args.command == 'doctor':
        if doctor(c): sys.exit(1)
    elif args.command == 'fetch-tools': fetch_tools(c)
    elif args.command == 'init-db': init_db(c)
    elif args.command == 'import-assets': import_assets(c)
    elif args.command == 'install-apk':
        if not c['patched_apk'] or not Path(c['patched_apk']).is_file(): raise RuntimeError('Set patched_apk to your prepared APK')
        run([c['adb'],'connect',c['serial']],capture_output=True,timeout=10)
        print(adb(c,'install','--no-incremental','-r',c['patched_apk']))

if __name__ == '__main__':
    try: main()
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError, psutil.Error) as e:
        print('ERROR:', e, file=sys.stderr); sys.exit(1)
