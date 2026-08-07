#!/usr/bin/env python3
"""Local server that resolves extensionless URLs the way GitHub Pages does.

Site URLs dropped their `.html` on 2026-08-07. GitHub Pages serves `/foo` from
`foo.html`; `python3 -m http.server` does not, so every internal link 404s under
the plain stdlib server and a Lighthouse run measures a broken page.

    python3 _tools/serve.py 8123

Lives under `_tools/` so Jekyll skips it — see CLAUDE.md, "What is public".
"""
import os, sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class PagesHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = super().translate_path(path)
        if not os.path.exists(local) and not path.rstrip('/').endswith('/'):
            candidate = local + '.html'
            if os.path.isfile(candidate):
                return candidate
        return local

    def send_error(self, code, message=None, explain=None):
        if code == 404 and os.path.isfile('404.html'):
            body = open('404.html', 'rb').read()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)
            return
        super().send_error(code, message, explain)

    def log_message(self, *args):
        pass


port = int(sys.argv[1]) if len(sys.argv) > 1 else 8123
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
print('serving %s on http://localhost:%d (extensionless URLs resolved)' % (root, port))
ThreadingHTTPServer(('', port), partial(PagesHandler, directory=root)).serve_forever()
