"""ADB transport selection, independent of the emulator vendor."""
import re
import subprocess
from platform_support import HIDDEN

def validate_serial(serial):
    if not isinstance(serial,str) or not re.fullmatch(r'[A-Za-z0-9_\[\]][A-Za-z0-9_.:\[\]-]{0,199}',serial):
        raise ValueError('serial must be auto or a device ID from adb devices (no spaces/options)')
    if ':' in serial and not re.fullmatch(r'(?:\[[0-9a-fA-F:]+\]|[A-Za-z0-9_.-]+):[0-9]+',serial):
        raise ValueError('Invalid ADB TCP endpoint; use host:port or [IPv6]:port')
    if ':' in serial and not 1 <= int(serial.rsplit(':',1)[1]) <= 65535:
        raise ValueError('Invalid ADB TCP port')
    return serial

def adb_command(c,*args,selected=True,timeout=15):
    command = [c['adb']]
    if selected: command += ['-s',c['serial']]
    return subprocess.run(command+list(args),check=True,capture_output=True,text=True,
                          timeout=timeout,creationflags=HIDDEN).stdout

def parse_devices(output):
    result=[]
    for line in output.splitlines():
        parts=line.split()
        if len(parts)>=2 and parts[1] in ('device','offline','unauthorized','recovery','sideload'):
            result.append((parts[0],parts[1]))
    return result

def resolve_device(c):
    wanted = c['serial']
    if wanted != 'auto' and ':' in wanted:
        adb_command(c,'connect',wanted,selected=False)
    devices = parse_devices(adb_command(c,'devices',selected=False))
    if wanted == 'auto':
        # Count unavailable devices too: never silently select one of several.
        if len(devices)>1: raise ValueError('Multiple ADB devices. Set serial explicitly: '+', '.join(x[0] for x in devices))
        if not devices: raise RuntimeError('No ADB device. Start an emulator or connect a device first.')
        wanted,status=devices[0]
    else:
        status=next((state for serial,state in devices if serial==wanted),None)
    if status != 'device': raise RuntimeError(f'ADB device {wanted}: {status or "not found"}. Check ADB/debugging authorization.')
    return wanted

def emulator_start_command(c):
    if c.get('emulator_start'): return c['emulator_start']
    # Compatibility with configurations created by the first Windows release.
    if c.get('emulator_manager'):
        return [c['emulator_manager'],'control','--vmindex',str(c['emulator_index']),'launch']
    return []
