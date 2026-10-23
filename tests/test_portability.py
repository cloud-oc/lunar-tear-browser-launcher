"""Offline tests: no emulator, network downloads or host service startup."""
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from app_config import ROOT,load_config
from android_device import validate_serial,parse_devices,resolve_device,emulator_start_command
from platform_support import host_target,server_release,extract_server

class PlatformTests(unittest.TestCase):
    def test_all_upstream_targets(self):
        for system,arch in [('Windows','AMD64'),('Darwin','x86_64'),('Darwin','arm64'),('Linux','x86_64'),('Linux','aarch64')]:
            _,name,url,digest=server_release(system,arch)
            self.assertTrue(url.endswith(name))
            self.assertEqual(len(digest),64)
        with self.assertRaises(RuntimeError): host_target('Windows','arm64')

    def test_safe_tar_retains_executable(self):
        with tempfile.TemporaryDirectory() as temp:
            archive=Path(temp)/'server.tar.gz'
            with tarfile.open(archive,'w:gz') as tar:
                info=tarfile.TarInfo('release/bin/dev'); info.size=4;info.mode=0o755
                tar.addfile(info,io.BytesIO(b'test'))
            extract_server(archive,Path(temp)/'out','release')
            self.assertEqual((Path(temp)/'out/bin/dev').read_bytes(),b'test')

    def test_tar_traversal_and_links_rejected(self):
        for path,link in [('release/../../outside',False),('release/bin/evil',True)]:
            with tempfile.TemporaryDirectory() as temp:
                archive=Path(temp)/'server.tar.gz'
                with tarfile.open(archive,'w:gz') as tar:
                    info=tarfile.TarInfo(path)
                    if link: info.type=tarfile.SYMTYPE;info.linkname='/tmp/escape'
                    tar.addfile(info)
                with self.assertRaises(RuntimeError): extract_server(archive,Path(temp)/'out','release')

class DeviceTests(unittest.TestCase):
    def test_serial_forms(self):
        for serial in ['auto','emulator-5554','127.0.0.1:16384','192.168.1.8:5555','[::1]:5555','R58M123456']:
            self.assertEqual(validate_serial(serial),serial)
        for serial in ['', '-d','foo bar','localhost:99999','host:bad','a;echo']:
            with self.assertRaises(ValueError): validate_serial(serial)

    @patch('android_device.adb_command')
    def test_auto_single_device(self,call):
        call.return_value='List of devices attached\nemulator-5554\tdevice\n'
        self.assertEqual(resolve_device({'serial':'auto'}),'emulator-5554')

    @patch('android_device.adb_command')
    def test_auto_multiple_devices_requires_choice(self,call):
        call.return_value='List of devices attached\none\tdevice\ntwo\tunauthorized\n'
        with self.assertRaises(ValueError): resolve_device({'serial':'auto'})

    @patch('android_device.adb_command')
    def test_emulator_serial_does_not_tcp_connect(self,call):
        call.return_value='List of devices attached\nemulator-5554\tdevice\n'
        resolve_device({'serial':'emulator-5554'})
        self.assertEqual(call.call_count,1)
        self.assertEqual(call.call_args.args[1],'devices')

    @patch('android_device.adb_command')
    def test_tcp_connect(self,call):
        call.return_value='List of devices attached\n127.0.0.1:5555\tdevice\n'
        resolve_device({'serial':'127.0.0.1:5555'})
        self.assertEqual(call.call_args_list[0].args[1],'connect')

    def test_vendor_neutral_command_and_old_mumu_config(self):
        self.assertEqual(emulator_start_command({'emulator_start':['emulator','-avd','Game']}),['emulator','-avd','Game'])
        self.assertEqual(emulator_start_command({'emulator_manager':'MuMuManager.exe','emulator_index':2})[-2:],['2','launch'])
        self.assertEqual(emulator_start_command({}),[])

    def test_config_accepts_path_command_and_audio_toggle(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'config.json'
            c=json.loads((ROOT/'config.example.json').read_text())
            c.update(adb='adb',serial='emulator-5554',audio=False,emulator_start=['emulator','-avd','Game'])
            path.write_text(json.dumps(c))
            loaded=load_config(path)
            self.assertFalse(loaded['audio'])
            self.assertEqual(loaded['emulator_start'][1:],['-avd','Game'])
