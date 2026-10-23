"""Portable configuration: relative paths are relative to the config file."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKAGE = 'com.square_enix.android_googleplay.nierspww'

def load_config(path=None):
    path = Path(path or ROOT/'config.json').resolve()
    c = json.loads(path.read_text(encoding='utf-8-sig'))
    for key in ('adb', 'emulator_manager', 'server_dir', 'scrcpy_server',
                'patched_apk', 'asset_archive', 'seven_zip'):
        value = c.get(key, '')
        if value:
            p = Path(value).expanduser()
            c[key] = str(p.resolve() if p.is_absolute() else (path.parent/p).resolve())
        else:
            c[key] = ''
    if not c['adb'] or not c['server_dir'] or not c['scrcpy_server']:
        raise ValueError('adb, server_dir and scrcpy_server are required')
    serial = c.get('serial', '')
    if not serial.startswith('127.0.0.1:') or not serial.split(':')[-1].isdigit():
        raise ValueError('serial must be a local emulator: 127.0.0.1:<port>')
    if not 1024 <= int(serial.split(':')[-1]) <= 65535:
        raise ValueError('Invalid emulator port')
    ports = c['ports']
    values = [ports[k] for k in ('web','grpc','cdn','auth','stream')]
    if any(type(p) is not int or not 1024 <= p <= 65535 for p in values):
        raise ValueError('Ports must be integers between 1024 and 65535')
    if len(set(values + [int(serial.split(':')[-1])])) != 6:
        raise ValueError('All service and emulator ports must be different')
    video = c['video']
    for k, low, high in [('max_size',320,3840),('max_fps',1,60),('bit_rate',100000,20000000)]:
        if type(video[k]) is not int or not low <= video[k] <= high:
            raise ValueError('Invalid video setting: '+k)
    if type(c.get('emulator_index')) is not int or c['emulator_index'] < 0:
        raise ValueError('emulator_index must be a nonnegative integer')
    c['_path'] = str(path)
    c['_runtime'] = str(path.parent/'runtime')
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
