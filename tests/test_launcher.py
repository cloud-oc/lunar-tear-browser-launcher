import copy
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from app_config import ROOT, load_config, asset_status
from launcher import init_db, owned_process

class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name)/'config.json'
        self.example = json.loads((ROOT/'config.example.json').read_text())

    def load(self):
        self.path.write_text(json.dumps(self.example))
        return load_config(self.path)

    def test_paths_are_relative_to_config(self):
        self.example['server_dir'] = 'space in path/server'
        self.assertEqual(self.load()['server_dir'],str((Path(self.temp.name)/'space in path/server').resolve()))

    def test_malformed_adb_target_rejected(self):
        self.example['serial'] = '-s other-device'
        with self.assertRaises(ValueError): self.load()

    def test_conflicting_ports_rejected(self):
        self.example['ports']['web'] = self.example['ports']['grpc']
        with self.assertRaises(ValueError): self.load()

    def test_new_database_and_existing_save_preserved(self):
        c = self.load()
        init_db(c)
        dbpath = Path(c['server_dir'])/'db/game.db'
        with closing(sqlite3.connect(dbpath)) as db:
            self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
            self.assertEqual(db.execute('SELECT COUNT(*) FROM goose_db_version').fetchone()[0],17)
            db.execute('CREATE TABLE user_preservation_test(value TEXT)')
            db.execute("INSERT INTO user_preservation_test VALUES ('keep this save')")
            db.commit()
        init_db(c)
        with closing(sqlite3.connect(dbpath)) as db:
            self.assertEqual(db.execute('SELECT value FROM user_preservation_test').fetchone()[0],'keep this save')

    def test_assets_require_master_and_android_catalog(self):
        c = self.load()
        root = Path(c['server_dir'])/'assets'
        (root/'revisions/0/android/assetbundle').mkdir(parents=True)
        (root/'revisions/0/android/list.bin').touch()
        self.assertFalse(asset_status(c)['ready'])
        (root/'release').mkdir()
        (root/'release/test.bin.e').touch()
        self.assertTrue(asset_status(c)['ready'])

    def test_stale_pid_cannot_be_stopped(self):
        import psutil
        p = psutil.Process()
        self.assertIsNone(owned_process({'pid':p.pid,'created':p.create_time()-10,'exe':p.exe()}))

if __name__ == '__main__': unittest.main()
