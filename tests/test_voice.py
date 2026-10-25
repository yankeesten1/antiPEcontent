import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from antipe.voice import prepare_voice


class VoiceIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.payload = b'trusted test model'
        self.models = {'test-model.bin': hashlib.sha256(self.payload).hexdigest()}

    def test_verified_cache_is_reused_without_network(self):
        with patch('antipe.voice.MODELS', self.models), patch('antipe.voice.urlopen', return_value=io.BytesIO(self.payload)) as request:
            prepare_voice(self.root)
            prepare_voice(self.root)
            self.assertEqual(request.call_count, 1)
        self.assertEqual((self.root / 'test-model.bin').read_bytes(), self.payload)

    def test_bad_download_is_rejected_and_partial_file_removed(self):
        with patch('antipe.voice.MODELS', self.models), patch('antipe.voice.urlopen', return_value=io.BytesIO(b'wrong bytes')):
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                prepare_voice(self.root)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_existing_corrupt_cache_is_preserved_and_not_loaded(self):
        file = self.root / 'test-model.bin'
        file.write_bytes(b'corrupt existing bytes')
        with patch('antipe.voice.MODELS', self.models), patch('antipe.voice.urlopen') as request:
            with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
                prepare_voice(self.root)
            request.assert_not_called()
        self.assertEqual(file.read_bytes(), b'corrupt existing bytes')


if __name__ == '__main__':
    unittest.main()
