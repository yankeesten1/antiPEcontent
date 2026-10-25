import base64
import io
import json
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from PIL import Image

from antipe.config import Settings
from antipe.generate import demo_drafts, research_sources, validate_drafts
from antipe.graphics import render_card
from antipe.instagram import Instagram
from antipe.service import due, local_day, make_batch
from antipe.store import Store, public_image_url
from antipe.web import create_server


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.settings = Settings(database=str(Path(self.temp.name) / 'data.db'), media_dir=str(Path(self.temp.name) / 'media'), meta_token='test-not-a-real-token', instagram_id='1234')
        self.store = Store(self.settings.database)

    def seed(self, kind='researched'):
        batch = self.store.claim_batch('2026-10-25', kind)
        self.store.finish_batch(batch, demo_drafts())
        draft = self.store.list_all()['drafts'][0]
        self.store.edit(draft['id'], draft['caption'], 'https://example.org/image.jpg', 1)
        return draft['id']

    def test_daily_batch_is_persisted_and_not_duplicated(self):
        self.assertTrue(make_batch(self.settings, self.store, demo=True))
        self.assertFalse(make_batch(self.settings, Store(self.settings.database), demo=True))
        self.assertEqual(len(self.store.list_all()['drafts']), 5)
        for draft in self.store.list_all()['drafts']:
            self.assertEqual(draft['kind'], 'demo')
        self.assertEqual(len(list(Path(self.settings.media_dir).glob('*.jpg'))), 5)

    def test_missing_key_records_failed_batch_and_retry_is_explicit(self):
        with self.assertRaisesRegex(ValueError, 'OPENAI_API_KEY'):
            make_batch(self.settings, self.store)
        self.assertEqual(self.store.list_all()['batches'][0]['status'], 'failed')
        self.assertFalse(make_batch(self.settings, self.store))
        with patch('antipe.service.generate', return_value=demo_drafts()):
            self.assertTrue(make_batch(self.settings, self.store, retry=True))
        self.assertEqual(len(self.store.list_all()['drafts']), 5)

    def test_schedule_handles_eastern_daylight_and_standard_time(self):
        self.assertFalse(due(self.settings, datetime(2026, 7, 2, 0, 59, tzinfo=timezone.utc)))
        self.assertTrue(due(self.settings, datetime(2026, 7, 2, 1, 0, tzinfo=timezone.utc)))
        self.assertEqual(local_day(self.settings, datetime(2026, 7, 2, 1, 0, tzinfo=timezone.utc)), '2026-07-01')
        self.assertFalse(due(self.settings, datetime(2026, 12, 2, 1, 59, tzinfo=timezone.utc)))
        self.assertTrue(due(self.settings, datetime(2026, 12, 2, 2, 0, tzinfo=timezone.utc)))

    def test_edit_invalidates_approval_and_stale_edits_fail(self):
        draft_id = self.seed()
        self.store.approve(draft_id, 2)
        self.store.edit(draft_id, 'Updated opinion with evidence.', 'https://example.org/new.jpg', 2)
        draft = self.store.get(draft_id)
        self.assertEqual(draft['status'], 'draft')
        self.assertIsNone(draft['approved_revision'])
        with self.assertRaises(ValueError):
            self.store.claim_publish(draft_id)
        with self.assertRaises(ValueError):
            self.store.edit(draft_id, 'Stale', 'https://example.org/image.jpg', 2)

    def test_demo_cannot_be_approved(self):
        with self.assertRaisesRegex(ValueError, 'Sample'):
            self.store.approve(self.seed('demo'), 2)

    def test_only_one_choice_per_batch_and_published_choice_is_final(self):
        first = self.seed()
        second = first - 1
        self.store.edit(second, 'Another caption', 'https://example.org/other.jpg', 1)
        self.store.approve(first, 2)
        self.store.approve(second, 2)
        self.assertEqual(self.store.get(first)['status'], 'draft')
        self.store.claim_publish(second)
        with self.assertRaises(ValueError):
            self.store.approve(first, 2)

    def test_publish_uses_approved_caption_and_blocks_duplicate(self):
        draft_id = self.seed()
        self.store.approve(draft_id, 2)
        instagram = Instagram(self.settings)
        with patch.object(instagram, 'request', side_effect=[{'id': 'container1'}, {'status_code': 'FINISHED'}, {'id': 'media1'}]) as request:
            self.assertEqual(instagram.publish(self.store, draft_id), 'media1')
            self.assertEqual(request.call_args_list[0].args[1]['caption'], self.store.get(draft_id)['caption'])
            with self.assertRaises(ValueError):
                instagram.publish(self.store, draft_id)
            self.assertEqual(request.call_count, 3)
        self.assertEqual(self.store.get(draft_id)['status'], 'published')

    def test_uncertain_publish_is_not_automatically_retried(self):
        draft_id = self.seed()
        self.store.approve(draft_id, 2)
        instagram = Instagram(self.settings)
        with patch.object(instagram, 'request', side_effect=[{'id': 'container1'}, {'status_code': 'FINISHED'}, TimeoutError()]):
            with self.assertRaises(TimeoutError):
                instagram.publish(self.store, draft_id)
        draft = self.store.get(draft_id)
        self.assertEqual(draft['status'], 'publish_unknown')
        self.assertEqual(draft['container_id'], 'container1')
        with self.assertRaises(ValueError):
            instagram.publish(self.store, draft_id)

    def test_caption_and_image_constraints(self):
        draft_id = self.seed()
        with self.assertRaises(ValueError):
            self.store.edit(draft_id, 'x' * 2201, 'https://example.org/image.jpg', 2)
        for url in ['http://example.org/a.jpg', 'https://127.0.0.1/a.jpg', 'https://localhost/a.jpg', 'https://user:pass@example.org/a.jpg']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                public_image_url(url)

    def test_graphic_is_real_square_jpeg_and_repeatable(self):
        filename = render_card(self.settings.media_dir, 'Who benefits from a buyout?')
        file = Path(self.settings.media_dir) / filename
        before = file.read_bytes()
        self.assertEqual(render_card(self.settings.media_dir, 'Who benefits from a buyout?'), filename)
        self.assertEqual(before, file.read_bytes())
        with Image.open(file) as image:
            self.assertEqual(image.size, (1080, 1080))
            self.assertEqual(image.format, 'JPEG')

    def test_generated_source_ids_must_match_actual_research(self):
        sources = [{'url': 'https://example.org/study', 'title': 'Study'}]
        data = {'drafts': [{'title': 'Title', 'caption': 'Supported opinion', 'image_brief': 'A card', 'source_ids': [0]} for _ in range(5)]}
        drafts = validate_drafts(data, sources)
        self.assertIn(sources[0]['url'], drafts[0]['caption'])
        data['drafts'][0]['source_ids'] = [99]
        with self.assertRaises(ValueError):
            validate_drafts(data, sources)

    def test_research_only_accepts_actual_https_citations(self):
        response = {'output': [{'content': [{'annotations': [{'type': 'url_citation', 'url': 'https://example.org/study', 'title': 'Study'}, {'type': 'url_citation', 'url': 'javascript:bad'}]}]}]}
        self.assertEqual(research_sources(response), [{'title': 'Study', 'url': 'https://example.org/study'}])

    def test_http_sample_workflow_csrf_and_images(self):
        server = create_server(self.settings, self.store, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        origin = f'http://127.0.0.1:{server.server_port}'
        with urlopen(origin + '/') as response:
            self.assertIn(b'Follow the money', response.read())
        with urlopen(origin + '/api/inbox') as response:
            inbox = json.load(response)
        self.assertNotIn(self.settings.meta_token, json.dumps(inbox))
        with self.assertRaises(HTTPError) as denied:
            urlopen(Request(origin + '/api/demo', data=b'{}', headers={'Content-Type': 'application/json'}))
        self.assertEqual(denied.exception.code, 403)
        with urlopen(Request(origin + '/api/demo', data=b'{}', headers={'X-CSRF-Token': inbox['csrf']})) as response:
            self.assertTrue(json.load(response)['created'])
        with urlopen(origin + '/api/inbox') as response:
            drafts = json.load(response)['drafts']
        self.assertEqual(len(drafts), 5)
        with urlopen(origin + f"/api/drafts/{drafts[0]['id']}/image") as response:
            with Image.open(io.BytesIO(response.read())) as image:
                self.assertEqual(image.format, 'JPEG')

    def test_public_binding_requires_password(self):
        with self.assertRaises(ValueError):
            create_server(self.settings, self.store, host='0.0.0.0', port=0)

    def test_inbox_auth_does_not_block_public_media(self):
        from dataclasses import replace
        settings = replace(self.settings, password='test-password')
        server = create_server(settings, self.store, port=0)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        origin = f'http://127.0.0.1:{server.server_port}'
        with self.assertRaises(HTTPError) as denied:
            urlopen(origin + '/api/inbox')
        self.assertEqual(denied.exception.code, 401)
        auth = base64.b64encode(b'editor:test-password').decode()
        with urlopen(Request(origin + '/api/inbox', headers={'Authorization': f'Basic {auth}'})) as response:
            self.assertIn('csrf', json.load(response))
        filename = render_card(settings.media_dir, 'Public post graphic')
        with urlopen(origin + '/media/' + filename) as response:
            self.assertEqual(response.headers['Content-Type'], 'image/jpeg')


if __name__ == '__main__':
    unittest.main()
