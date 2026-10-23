"""Portable configuration: relative paths are relative to the config file."""
import json
import hashlib
from pathlib import Path
from platform_support import find_tool
from android_device import validate_serial

ROOT = Path(__file__).resolve().parent
PACKAGE = 'com.square_enix.android_googleplay.nierspww'

def load_config(path=None):
    path = Path(path or ROOT/'config.json').resolve()
    c = json.loads(path.read_text(encoding='utf-8-sig'))
    for key in ('emulator_manager', 'server_dir', 'scrcpy_server',
                'patched_apk', 'asset_archive'):
        value = c.get(key, '')
        if value:
            p = Path(value).expanduser()
            c[key] = str(p.resolve() if p.is_absolute() else (path.parent/p).resolve())
        else:
            c[key] = ''
    c['adb'] = find_tool(c.get('adb','auto'),'adb',path.parent)
    c['seven_zip'] = find_tool(c.get('seven_zip','auto'),'seven_zip',path.parent)
    if not c['adb'] or not c['server_dir'] or not c['scrcpy_server']:
        raise ValueError('adb, server_dir and scrcpy_server are required')
    serial = c['serial'] = validate_serial(c.get('serial','auto'))
    ports = c['ports']
    values = [ports[k] for k in ('web','grpc','cdn','auth','stream')]
    if any(type(p) is not int or not 1024 <= p <= 65535 for p in values):
        raise ValueError('Ports must be integers between 1024 and 65535')
    local_port = [int(serial.rsplit(':',1)[1])] if serial.startswith(('127.0.0.1:','localhost:','[::1]:')) else []
    if len(set(values+local_port)) != len(values+local_port):
        raise ValueError('All service and emulator ports must be different')
    video = c['video']
    for k, low, high in [('max_size',320,3840),('max_fps',1,60),('bit_rate',100000,20000000)]:
        if type(video[k]) is not int or not low <= video[k] <= high:
            raise ValueError('Invalid video setting: '+k)
    c.setdefault('emulator_index',0)
    if type(c['emulator_index']) is not int or c['emulator_index'] < 0:
        raise ValueError('emulator_index must be a nonnegative integer')
    c['_path'] = str(path)
    command = c.get('emulator_start',[])
    if not isinstance(command,list) or any(not isinstance(x,str) or not x or '\x00' in x for x in command):
        raise ValueError('emulator_start must be an argv array, not a shell command')
    if command:
        command = command.copy()
        command[0] = find_tool(command[0],'emulator',path.parent)
    c['emulator_start'] = command
    c.setdefault('boot_timeout',180)
    if type(c['boot_timeout']) is not int or not 10 <= c['boot_timeout'] <= 900:
        raise ValueError('boot_timeout must be 10..900 seconds')
    c.setdefault('audio',True)
    if type(c['audio']) is not bool: raise ValueError('audio must be true or false')
    suffix = '' if path.name == 'config.json' else hashlib.sha256(str(path).encode()).hexdigest()[:12]
    c['_runtime'] = str(path.parent/'runtime'/suffix)
    return c

def asset_status(c):
    root = Path(c['server_dir'])/'assets'
    revision = root/'revisions/0'
    candidates = [revision/'android', revision]
    assets = any((p/'list.bin').is_file() and (p/'assetbundle').is_dir()
                 for p in candidates)
    master = any((root/'release').glob('*.bin.e'))
    return {'ready': bool(assets and master), 'assets': assets, 'master': master,
            'message': 'Resource layout found; gameplay still depends on complete assets.' if assets and master
            else 'Prepare Android assets and patched master data; see README.'}
