import json
import re
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class Instagram:
    """Meta Instagram API with Facebook Login (professional accounts only)."""
    def __init__(self, settings):
        self.settings = settings

    def request(self, path, data=None):
        if not re.fullmatch(r"v\d+\.\d+", self.settings.meta_version):
            raise ValueError("Invalid META_API_VERSION")
        request = Request(
            f"https://graph.facebook.com/{self.settings.meta_version}/{path}",
            data=urlencode(data).encode() if data is not None else None,
            headers={"Authorization": f"Bearer {self.settings.meta_token}"},
        )
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except Exception as error:
            raise RuntimeError(f"Meta request failed ({getattr(error, 'code', type(error).__name__)}). Check account permissions, image requirements and token validity in Meta.") from None

    def publish(self, store, draft_id):
        if not self.settings.meta_token or not self.settings.instagram_id:
            raise ValueError("Configure META_ACCESS_TOKEN and INSTAGRAM_ACCOUNT_ID before publishing")
        if not self.settings.instagram_id.isdigit():
            raise ValueError("INSTAGRAM_ACCOUNT_ID must be the numeric professional account ID")
        draft = store.claim_publish(draft_id)
        try:
            container = self.request(f"{self.settings.instagram_id}/media", {"image_url": draft['image_url'], "caption": draft['caption']})['id']
            store.publication(draft_id, 'publishing', container_id=container)
            for _ in range(12):
                state = self.request(f"{container}?fields=status_code").get('status_code')
                if state == 'FINISHED':
                    break
                if state in ('ERROR', 'EXPIRED'):
                    raise RuntimeError(f"Instagram image processing returned {state}")
                time.sleep(5)
            else:
                raise RuntimeError("Instagram image processing did not finish within one minute")
            media = self.request(f"{self.settings.instagram_id}/media_publish", {"creation_id": container})['id']
            store.publication(draft_id, 'published', media_id=media)
            return media
        except Exception:
            # A network timeout might happen after Meta commits the publication.
            # Block automatic retries so an uncertain result cannot create duplicates.
            store.publication(draft_id, 'publish_unknown', error="Publication did not complete locally. Check the Instagram account and Meta container status before any manual recovery. Automatic retry is disabled.")
            raise
