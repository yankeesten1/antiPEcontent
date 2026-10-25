import csv
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from PIL import Image

from antipe.pilot import DEFAULT_BATCH, export_pilot
from antipe.launch import BIO, review_html


class PilotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_offline_kit_contains_seven_images_captions_and_trackers(self):
        output = self.root / 'week-01'
        with patch('antipe.generate.urlopen', side_effect=AssertionError('No network permitted')) as model, patch('antipe.instagram.urlopen', side_effect=AssertionError('No network permitted')) as meta:
            archive = export_pilot(output)
            model.assert_not_called()
            meta.assert_not_called()
        self.assertEqual(len(list(output.glob('*.jpg'))), 7)
        captions = list(output.glob('*-caption.txt'))
        self.assertEqual(len(captions), 7)
        self.assertTrue(all(0 < len(caption.read_text().strip()) <= 2200 for caption in captions))
        for image in output.glob('*.jpg'):
            with Image.open(image) as opened:
                self.assertEqual(opened.size, (1080, 1080))
                self.assertEqual(opened.format, 'JPEG')
        with (output / 'metrics.csv').open() as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 7)
        self.assertTrue(all(row['reach_48h'] == '' for row in rows))
        with (output / 'weekly-review.csv').open() as handle:
            self.assertEqual(len(list(csv.DictReader(handle))), 8)
        with zipfile.ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertEqual(len([name for name in bundle.namelist() if name.endswith('.jpg')]), 7)
            self.assertIn('week-01/START-HERE.md', bundle.namelist())
        review = (output / 'REVIEW-BEFORE-PUBLISHING.md').read_text()
        self.assertEqual(review.count('Approval: **not approved**'), 7)
        self.assertIn('not retrieved; verify before publication', review)

    def test_export_never_overwrites_editor_changes(self):
        output = self.root / 'week-01'
        export_pilot(output)
        edited = output / '01-w01-01-caption.txt'
        edited.write_text('My edited caption')
        with self.assertRaisesRegex(ValueError, 'already exists'):
            export_pilot(output)
        self.assertEqual(edited.read_text(), 'My edited caption')

    def test_invalid_caption_and_paths_fail_before_writing(self):
        batch = json.loads(DEFAULT_BATCH.read_text())
        batch['posts'][0]['caption'] = 'x' * 2201
        custom = self.root / 'custom.json'
        custom.write_text(json.dumps(batch))
        with self.assertRaisesRegex(ValueError, 'caption limit'):
            export_pilot(self.root / 'invalid', custom)
        self.assertFalse((self.root / 'invalid').exists())
        batch['posts'][0]['caption'] = 'An opinion.'
        batch['posts'][0]['id'] = '../../outside'
        custom.write_text(json.dumps(batch))
        with self.assertRaisesRegex(ValueError, 'Post IDs'):
            export_pilot(self.root / 'invalid', custom)

    def test_launch_assets_include_usable_avatar_and_offline_editor(self):
        output = self.root / 'tonight'
        archive = export_pilot(output, launch_assets=True)
        self.assertLessEqual(len(BIO), 150)
        with Image.open(output / 'profile-avatar-1080.png') as avatar:
            self.assertEqual(avatar.size, (1080, 1080))
            self.assertEqual(avatar.format, 'PNG')
        with Image.open(output / 'profile-avatar-320.png') as avatar:
            self.assertEqual(avatar.size, (320, 320))
        html = (output / 'review.html').read_text()
        self.assertEqual(html.count('<textarea '), 7)
        self.assertEqual(html.count('data-editor='), 7)
        self.assertIn('Edits are not saved automatically', html)
        self.assertNotIn('fetch(', html)
        self.assertIn('not approved', (output / 'FIRST-POST-REVIEW.md').read_text())
        with zipfile.ZipFile(archive) as bundle:
            self.assertIsNone(bundle.testzip())
            self.assertIn('tonight/review.html', bundle.namelist())
            self.assertIn('tonight/TONIGHT.md', bundle.namelist())

    def test_offline_review_escapes_untrusted_content(self):
        batch = json.loads(DEFAULT_BATCH.read_text())
        batch['posts'][0]['title'] = '<img src=x onerror=alert(1)>'
        batch['posts'][0]['caption'] = '</textarea><script>alert(1)</script>'
        html = review_html(batch)
        self.assertNotIn('<img src=x', html)
        self.assertNotIn('</textarea><script>alert', html)
        self.assertIn('&lt;/textarea&gt;&lt;script&gt;', html)


if __name__ == '__main__':
    unittest.main()
