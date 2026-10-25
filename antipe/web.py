import base64
import hmac
import json
import re
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .graphics import render_card
from .instagram import Instagram
from .service import make_batch, scheduler

STATIC = Path(__file__).resolve().parent.parent / 'static'


def create_server(settings, store, host='127.0.0.1', port=8000):
    if host not in ('127.0.0.1', 'localhost', '::1') and not settings.password:
        raise ValueError("Set ANTIPE_PASSWORD before listening outside localhost; use HTTPS through a reverse proxy")
    csrf = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            # No URL queries, credentials, captions or API payloads in access logs.
            pass

        def send(self, code, body, content_type='application/json; charset=utf-8'):
            if isinstance(body, (dict, list)):
                body = json.dumps(body).encode()
            elif isinstance(body, str):
                body = body.encode()
            self.send_response(code)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; img-src 'self' https:; style-src 'self'; script-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            self.end_headers()
            self.wfile.write(body)

        def authorized(self):
            if not settings.password:
                # A loopback-only app should not accept an attacker-controlled Host
                # through browser DNS rebinding.
                hostname = urlparse('http://' + self.headers.get('Host', '')).hostname
                if hostname not in ('localhost', '127.0.0.1', '::1'):
                    self.send(403, {"error": "Local inbox requires a localhost Host header"})
                    return False
                return True
            try:
                kind, encoded = self.headers.get('Authorization', '').split(' ', 1)
                _, password = base64.b64decode(encoded, validate=True).decode().split(':', 1)
                if kind.lower() == 'basic' and hmac.compare_digest(password.encode(), settings.password.encode()):
                    return True
            except (ValueError, UnicodeError):
                pass
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="PE editorial inbox", charset="UTF-8"')
            self.send_header('Content-Length', '0')
            self.end_headers()
            return False

        def do_GET(self):
            path = urlparse(self.path).path
            # Meta must be able to fetch only these public post graphics without login.
            if re.fullmatch(r'/media/[a-f0-9]{64}\.jpg', path):
                file = Path(settings.media_dir) / path.rsplit('/', 1)[1]
                if file.is_file():
                    self.send(200, file.read_bytes(), 'image/jpeg')
                else:
                    self.send(404, {"error": "Image not found"})
                return
            if not self.authorized():
                return
            if path == '/':
                self.send(200, (STATIC / 'index.html').read_bytes(), 'text/html; charset=utf-8')
            elif path in ('/app.js', '/style.css'):
                self.send(200, (STATIC / path[1:]).read_bytes(), 'application/javascript' if path.endswith('.js') else 'text/css')
            elif path == '/api/inbox':
                self.send(200, {**store.list_all(), "csrf": csrf, "settings": {
                    "timezone": settings.timezone, "daily_time": settings.daily_time,
                    "generation_configured": bool(settings.openai_key),
                    "publishing_configured": bool(settings.meta_token and settings.instagram_id),
                    "public_url_configured": bool(settings.public_base),
                }})
            elif match := re.fullmatch(r'/api/drafts/(\d+)/image', path):
                try:
                    draft = store.get(int(match[1]))
                    file = Path(settings.media_dir) / render_card(settings.media_dir, draft['title'])
                    self.send(200, file.read_bytes(), 'image/jpeg')
                except ValueError:
                    self.send(404, {"error": "Draft not found"})
            else:
                self.send(404, {"error": "Not found"})

        def do_POST(self):
            if not self.authorized():
                return
            if not hmac.compare_digest(self.headers.get('X-CSRF-Token', ''), csrf):
                self.send(403, {"error": "Refresh the inbox before making changes"})
                return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 20000:
                    raise ValueError("Invalid request size")
                data = json.loads(self.rfile.read(size))
                if not isinstance(data, dict):
                    raise ValueError("Expected a JSON object")
                path = urlparse(self.path).path
                if path in ('/api/generate', '/api/demo'):
                    if path == '/api/generate' and not settings.openai_key:
                        raise ValueError("Set OPENAI_API_KEY securely before generating researched posts")
                    created = make_batch(settings, store, demo=path == '/api/demo')
                    self.send(200, {"created": created})
                    return
                match = re.fullmatch(r'/api/drafts/(\d+)/(edit|approve|publish)', path)
                if not match:
                    self.send(404, {"error": "Not found"})
                    return
                draft_id, action = int(match[1]), match[2]
                if action == 'edit':
                    store.edit(draft_id, data['caption'], data['image_url'], int(data['revision']))
                elif action == 'approve':
                    store.approve(draft_id, int(data['revision']))
                else:
                    Instagram(settings).publish(store, draft_id)
                self.send(200, {"ok": True})
            except (ValueError, KeyError, TypeError) as error:
                self.send(400, {"error": str(error)})
            except Exception:
                self.send(502, {"error": "Operation failed. See batch or draft status for recovery instructions; check provider configuration."})

    return ThreadingHTTPServer((host, port), Handler)


def serve(settings, store, host, port, scheduled=True):
    server = create_server(settings, store, host, port)
    stop = threading.Event()
    if scheduled:
        threading.Thread(target=scheduler, args=(settings, store, stop), daemon=True).start()
    print(f"Editorial inbox listening on port {server.server_port}; daily drafts at {settings.daily_time} {settings.timezone}. Keep this process running for scheduling.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()
