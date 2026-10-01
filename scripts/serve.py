"""Local dev server that tells the browser never to cache, so edits show up on a normal reload.
Usage: python3 scripts/serve.py [port]   (serves the project root; port falls back to $PORT, then 5173)
"""
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class NoCacheHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    # Port: CLI argument, else the PORT env var (set by the preview launcher), else 5173
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 5173))
    print(f"Serving on http://localhost:{port} (no-cache)")
    ThreadingHTTPServer(("", port), NoCacheHandler).serve_forever()
