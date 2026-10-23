"""Host tools and safe, version-pinned server installation."""
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import tarfile
import zipfile

HIDDEN = 0x08000000 if os.name == 'nt' else 0
SERVER_HASHES = {
    ('windows','amd64'): 'd8f6330a8f3a8788a89ba8ecfc01a5ff40ab566a9c46d9ff6fd0929503dd5f0a',
    ('darwin','amd64'): '483a323361e764e1ff1b5415f54423a28d1efacf52cea2f89917037023b598c7',
    ('darwin','arm64'): '4d090ce972dd8031072efb79c9b126ed57cf3464fbcf505d3f837983fe2dc4c8',
    ('linux','amd64'): 'd1b08d5bd11959209baa230f2e9de00685e54a0affbf4c7518c0942d99beca12',
    ('linux','arm64'): '444641b7efacee8f0106ed3c0177a1c92cf88f161a69c5841437bb3cb8384809',
}

def host_target(system=None, machine=None):
    system = (system or platform.system()).lower()
    machine = (machine or platform.machine()).lower()
    arch = {'x86_64':'amd64','amd64':'amd64','aarch64':'arm64','arm64':'arm64'}.get(machine,machine)
    if (system,arch) not in SERVER_HASHES:
        raise RuntimeError(f'No pinned upstream binary for {system}/{arch}. Supported: Windows x64, macOS/Linux x64 and arm64.')
    return system,arch

def server_release(system=None, machine=None):
    system,arch = host_target(system,machine)
    name = f'lunar-tear-server-v1.0.2-{system}-{arch}'
    filename = name+('.zip' if system == 'windows' else '.tar.gz')
    return name, filename, 'https://github.com/Walter-Sparrow/lunar-tear/releases/download/v1.0.2/'+filename, SERVER_HASHES[(system,arch)]

def binary(server_dir, name):
    return Path(server_dir)/'bin'/(name+('.exe' if os.name == 'nt' else ''))

def find_tool(value, tool, base):
    """Resolve an explicit path, PATH command or Android SDK installation."""
    if value and value != 'auto':
        expanded = os.path.expandvars(os.path.expanduser(value))
        if '/' not in expanded and '\\' not in expanded:
            return shutil.which(expanded) or expanded
        p = Path(expanded)
        return str((p if p.is_absolute() else base/p).resolve())
    names = ['adb'] if tool == 'adb' else ['7zz','7z']
    for name in names:
        located = shutil.which(name)
        if located: return located
    if tool == 'adb':
        roots = [os.environ.get('ANDROID_HOME'),os.environ.get('ANDROID_SDK_ROOT'),
                 str(Path.home()/'Library/Android/sdk'),str(Path.home()/'Android/Sdk')]
        if os.environ.get('LOCALAPPDATA'): roots.append(str(Path(os.environ['LOCALAPPDATA'])/'Android/Sdk'))
        for root in filter(None,roots):
            candidate = Path(root)/'platform-tools'/('adb.exe' if os.name == 'nt' else 'adb')
            if candidate.is_file(): return str(candidate)
    elif os.name == 'nt':
        candidate = Path(os.environ.get('ProgramFiles','C:/Program Files'))/'7-Zip/7z.exe'
        if candidate.is_file(): return str(candidate)
    return names[0]

def extract_server(archive, destination, prefix):
    """Extract only regular files/directories. Never honor archive links or modes."""
    root = Path(destination).resolve()
    root.mkdir(parents=True,exist_ok=True)
    def target(name):
        p = PurePosixPath(name)
        if '\\' in name or ':' in name or p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] != prefix:
            raise RuntimeError('Unsafe server archive path: '+name)
        result = root.joinpath(*p.parts[1:]).resolve()
        if not result.is_relative_to(root): raise RuntimeError('Archive path escapes destination')
        return result
    if str(archive).endswith('.zip'):
        with zipfile.ZipFile(archive) as z:
            for item in z.infolist():
                dst = target(item.filename)
                if item.is_dir(): dst.mkdir(parents=True,exist_ok=True)
                else:
                    dst.parent.mkdir(parents=True,exist_ok=True)
                    with z.open(item) as src,dst.open('xb') as out: shutil.copyfileobj(src,out)
    else:
        with tarfile.open(archive,'r:gz') as tar:
            for item in tar:
                dst = target(item.name)
                if item.isdir(): dst.mkdir(parents=True,exist_ok=True)
                elif item.isfile():
                    dst.parent.mkdir(parents=True,exist_ok=True)
                    with tar.extractfile(item) as src,dst.open('xb') as out: shutil.copyfileobj(src,out)
                    dst.chmod(0o755 if item.mode & 0o111 else 0o644)
                else: raise RuntimeError('Archive links/devices are not supported')
