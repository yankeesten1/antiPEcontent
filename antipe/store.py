import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from urllib.parse import urlparse


def now():
    return datetime.now(timezone.utc).isoformat()


def public_image_url(value):
    import ipaddress
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Use a public HTTPS URL for the Instagram JPEG image")
    host = parsed.hostname.lower()
    if host == "localhost" or host.endswith((".local", ".localhost")):
        raise ValueError("The image URL must be publicly reachable by Meta")
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise ValueError("The image URL must be public")
    return value


class Store:
    def __init__(self, path):
        self.path = path
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS batches (
                    id INTEGER PRIMARY KEY, day TEXT NOT NULL, kind TEXT NOT NULL,
                    status TEXT NOT NULL, error TEXT, created_at TEXT NOT NULL,
                    UNIQUE(day, kind)
                );
                CREATE TABLE IF NOT EXISTS drafts (
                    id INTEGER PRIMARY KEY, batch_id INTEGER NOT NULL REFERENCES batches(id),
                    title TEXT NOT NULL, caption TEXT NOT NULL, image_brief TEXT NOT NULL,
                    sources TEXT NOT NULL, image_url TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL DEFAULT 'draft', revision INTEGER NOT NULL DEFAULT 1,
                    approved_revision INTEGER, container_id TEXT, instagram_media_id TEXT,
                    error TEXT, updated_at TEXT NOT NULL
                );
            """)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        try:
            with db:
                yield db
        finally:
            db.close()

    def claim_batch(self, day, kind, retry=False):
        with self.connect() as db:
            if retry:
                db.execute("DELETE FROM batches WHERE day=? AND kind=? AND status='failed'", (day, kind))
            cursor = db.execute("INSERT OR IGNORE INTO batches(day,kind,status,created_at) VALUES (?,?,'generating',?)", (day, kind, now()))
            return cursor.lastrowid if cursor.rowcount else None

    def finish_batch(self, batch_id, drafts):
        with self.connect() as db:
            for draft in drafts:
                db.execute("INSERT INTO drafts(batch_id,title,caption,image_brief,sources,image_url,updated_at) VALUES (?,?,?,?,?,?,?)", (batch_id, draft['title'], draft['caption'], draft['image_brief'], json.dumps(draft['sources']), draft.get('image_url', ''), now()))
            db.execute("UPDATE batches SET status='ready', error=NULL WHERE id=?", (batch_id,))

    def fail_batch(self, batch_id, message):
        with self.connect() as db:
            db.execute("UPDATE batches SET status='failed', error=? WHERE id=?", (message, batch_id))

    def list_all(self):
        with self.connect() as db:
            drafts = [dict(row) for row in db.execute("SELECT d.*,b.kind,b.day FROM drafts d JOIN batches b ON b.id=d.batch_id ORDER BY d.id DESC")]
            for draft in drafts:
                draft['sources'] = json.loads(draft['sources'])
            return {"drafts": drafts, "batches": [dict(row) for row in db.execute("SELECT * FROM batches ORDER BY id DESC")]}

    def get(self, draft_id):
        with self.connect() as db:
            row = db.execute("SELECT d.*,b.kind FROM drafts d JOIN batches b ON b.id=d.batch_id WHERE d.id=?", (draft_id,)).fetchone()
            if not row:
                raise ValueError("Draft not found")
            result = dict(row)
            result['sources'] = json.loads(result['sources'])
            return result

    def edit(self, draft_id, caption, image_url, revision):
        if not isinstance(caption, str) or not caption.strip() or len(caption) > 2200:
            raise ValueError("Instagram captions must contain 1–2,200 characters")
        if image_url:
            public_image_url(image_url)
        with self.connect() as db:
            cursor = db.execute("""UPDATE drafts SET caption=?,image_url=?,revision=revision+1,
                status='draft',approved_revision=NULL,error=NULL,updated_at=?
                WHERE id=? AND revision=? AND status IN ('draft','approved')""", (caption.strip(), image_url, now(), draft_id, revision))
            if not cursor.rowcount:
                raise ValueError("Draft changed or cannot be edited. Refresh the inbox.")

    def approve(self, draft_id, revision):
        draft = self.get(draft_id)
        if draft['kind'] == 'demo':
            raise ValueError("Sample drafts cannot be published. Generate researched drafts first.")
        public_image_url(draft['image_url'])
        with self.connect() as db:
            # Selecting one draft reserves the day's publishing choice. Approval is a
            # durable snapshot; later edits invalidate it.
            db.execute("BEGIN IMMEDIATE")
            other = db.execute("SELECT id FROM drafts WHERE batch_id=? AND id<>? AND status IN ('publishing','published','publish_unknown')", (draft['batch_id'], draft_id)).fetchone()
            if other:
                raise ValueError("Another draft from this batch has already entered publishing")
            cursor = db.execute("UPDATE drafts SET status='approved',approved_revision=revision,updated_at=? WHERE id=? AND revision=? AND status IN ('draft','approved')", (now(), draft_id, revision))
            if not cursor.rowcount:
                raise ValueError("Draft changed or cannot be approved. Refresh the inbox.")
            db.execute("UPDATE drafts SET status='draft',approved_revision=NULL WHERE batch_id=? AND id<>? AND status='approved'", (draft['batch_id'], draft_id))

    def claim_publish(self, draft_id):
        with self.connect() as db:
            cursor = db.execute("UPDATE drafts SET status='publishing',error=NULL,updated_at=? WHERE id=? AND status='approved' AND approved_revision=revision", (now(), draft_id))
            if not cursor.rowcount:
                raise ValueError("Publishing requires the current revision's approval and cannot run twice")
        return self.get(draft_id)

    def publication(self, draft_id, status, container_id=None, media_id=None, error=None):
        with self.connect() as db:
            db.execute("UPDATE drafts SET status=?,container_id=COALESCE(?,container_id),instagram_media_id=COALESCE(?,instagram_media_id),error=?,updated_at=? WHERE id=?", (status, container_id, media_id, error, now(), draft_id))
