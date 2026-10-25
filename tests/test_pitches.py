import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from antipe.config import Settings
from antipe.generate import demo_drafts
from antipe.pitches import export_pitches
from antipe.store import Store


class PitchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.settings = Settings(database=str(self.root / 'state.sqlite3'))

    def test_sample_pack_has_five_choices_without_paid_calls(self):
        with patch('antipe.pitches.generate') as paid:
            folder = export_pitches(self.settings, '2026-10-25', self.root / 'pack', demo=True)
        paid.assert_not_called()
        self.assertIn('Pitch 5', (folder / 'review.html').read_text())
        self.assertIn('SAMPLE ONLY', (folder / 'review.html').read_text())
        self.assertFalse(list(folder.glob('*.mp4')))

    def test_generated_text_is_escaped_and_daily_rerun_does_not_spend(self):
        drafts = demo_drafts()
        drafts[0]['title'] = '<script>alert(1)</script>'
        with patch('antipe.pitches.generate', return_value=drafts) as paid:
            folder = export_pitches(self.settings, '2026-10-25', self.root / 'pack')
            with self.assertRaisesRegex(ValueError, 'already has a pitch batch'):
                export_pitches(self.settings, '2026-10-25', self.root / 'another')
        self.assertEqual(paid.call_count, 1)
        page = (folder / 'review.html').read_text()
        self.assertNotIn('<script>', page)
        self.assertIn('&lt;script&gt;', page)

    def test_failed_attempt_requires_review_before_retry(self):
        with patch('antipe.pitches.generate', side_effect=ValueError('provider failed')) as paid:
            with self.assertRaises(ValueError):
                export_pitches(self.settings, '2026-10-25', self.root / 'pack')
            with self.assertRaisesRegex(ValueError, 'already has a pitch batch'):
                export_pitches(self.settings, '2026-10-25', self.root / 'another')
        self.assertEqual(paid.call_count, 1)

    def test_candidate_cannot_enter_legacy_image_publishing_flow(self):
        with patch('antipe.pitches.generate', return_value=demo_drafts()):
            export_pitches(self.settings, '2026-10-25', self.root / 'pack')
        store = Store(self.settings.database)
        draft = store.list_all()['drafts'][0]
        with self.assertRaisesRegex(ValueError, 'not finished posts'):
            store.approve(draft['id'], draft['revision'])
