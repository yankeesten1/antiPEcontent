import array
import tempfile
import unittest
import wave
from pathlib import Path

from antipe.sound import join_narration, original_music


class SoundTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def wav(self, name, samples, rate=48000):
        path = self.root / name
        with wave.open(str(path), 'wb') as out:
            out.setnchannels(1)
            out.setsampwidth(2)
            out.setframerate(rate)
            out.writeframes(array.array('h', samples).tobytes())
        return path

    def test_narration_preserves_entire_spoken_waveform(self):
        values = [1000, -1000] * 1000
        source = self.wav('voice.wav', values)
        destination = self.root / 'joined.wav'
        join_narration([source], [24], destination)
        with wave.open(str(destination)) as audio:
            data = array.array('h', audio.readframes(audio.getnframes()))
            self.assertEqual(audio.getnframes(), 48000)
        self.assertEqual(list(data[7200:9200]), values)
        self.assertTrue(all(value == 0 for value in data[:7200]))
        self.assertTrue(all(value == 0 for value in data[9200:]))

    def test_long_narration_cannot_be_silently_cut_off(self):
        source = self.wav('long.wav', [1000] * 48000)
        with self.assertRaisesRegex(ValueError, 'instead of cutting speech'):
            join_narration([source], [24], self.root / 'joined.wav')

    def test_mismatched_audio_format_is_rejected(self):
        source = self.wav('wrong-rate.wav', [1000] * 100, rate=16000)
        with self.assertRaisesRegex(ValueError, '48 kHz'):
            join_narration([source], [24], self.root / 'joined.wav')

    def test_original_music_has_expected_duration_and_actual_sound(self):
        destination = self.root / 'music.wav'
        original_music(destination, .3)
        with wave.open(str(destination)) as audio:
            self.assertEqual(audio.getnframes(), 14400)
            self.assertEqual(audio.getframerate(), 48000)
            values = array.array('h', audio.readframes(audio.getnframes()))
        self.assertGreater(max(abs(value) for value in values), 0)
        self.assertLess(max(abs(value) for value in values), 32767)


if __name__ == '__main__':
    unittest.main()
