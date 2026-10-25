import json
import shutil
import tempfile
import unittest
from pathlib import Path

from antipe.cases import validate_case


class CaseEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        source = Path(__file__).resolve().parent.parent / 'pilot' / 'cases' / 'usap'
        self.root = Path(self.temp.name) / 'case'
        self.root.mkdir()
        shutil.copyfile(source / 'case.json', self.root / 'case.json')
        shutil.copytree(source / 'sources', self.root / 'sources')
        self.path = self.root / 'case.json'

    def test_reviewed_case_preserves_denial_and_dated_scope(self):
        case = validate_case(self.path)
        self.assertEqual(case['approval'], 'pending_user_review')
        self.assertIn('April 23, 2026', case['coverage'])
        self.assertTrue(any(claim['kind'] == 'party_denial' for claim in case['claims']))

    def test_invented_quotation_is_rejected(self):
        case = json.loads(self.path.read_text())
        case['quotes'][0]['exact_text'] = 'This quotation was never in the original record.'
        self.path.write_text(json.dumps(case))
        with self.assertRaisesRegex(ValueError, 'verbatim'):
            validate_case(self.path)

    def test_snapshot_change_blocks_case_before_rendering(self):
        case = json.loads(self.path.read_text())
        file = self.root / 'sources' / case['sources'][0]['snapshot']
        file.write_text(file.read_text() + '\nAn altered source snapshot.')
        with self.assertRaisesRegex(ValueError, 'snapshot changed'):
            validate_case(self.path)

    def test_snapshot_path_cannot_escape_case_sources(self):
        case = json.loads(self.path.read_text())
        case['sources'][0]['snapshot'] = '../case.json'
        self.path.write_text(json.dumps(case))
        with self.assertRaisesRegex(ValueError, 'within the case sources'):
            validate_case(self.path)
