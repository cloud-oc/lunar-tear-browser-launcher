import json
from pathlib import Path
import tempfile

from aiohttp.test_utils import AioHTTPTestCase
from app_config import ROOT, load_config
from bridge import create_app

class HttpTests(AioHTTPTestCase):
    async def get_application(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        path = Path(self.tmp.name)/'config.json'
        path.write_text((ROOT/'config.example.json').read_text())
        return create_app(load_config(path))

    async def test_status_local(self):
        response = await self.client.get('/status',headers={'Host':'127.0.0.1:18765'})
        self.assertEqual(response.status,200)
        self.assertFalse((await response.json())['ready'])

    async def test_host_rebinding_rejected(self):
        response = await self.client.get('/status',headers={'Host':'attacker.example:18765'})
        self.assertEqual(response.status,403)

    async def test_foreign_origin_rejected(self):
        response = await self.client.get('/stream',headers={'Host':'127.0.0.1:18765','Origin':'https://attacker.example'})
        self.assertEqual(response.status,403)

    async def test_missing_stream_origin_rejected(self):
        response = await self.client.get('/stream',headers={'Host':'127.0.0.1:18765'})
        self.assertEqual(response.status,403)
