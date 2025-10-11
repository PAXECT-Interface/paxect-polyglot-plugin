#!/usr/bin/env python3
# Demo 05 - iOS HTTP bridge ping (Python, cross-OS)
# Goal: POST a tiny payload to a (local) gateway at http://127.0.0.1:8765.
# Soft checks: if the gateway is not running -> friendly message, still ends with OK.
# Tip: set PAXECT_START_GATEWAY=1 to spin up a temporary internal gateway for testing.

import sys, os, time, json, threading, http.server, socketserver
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

# --- optional internal test gateway (host-only) ---
class _Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        import hashlib
        resp = {"ok": True, "sha256": hashlib.sha256(body).hexdigest(), "len": len(body)}
        data = json.dumps(resp).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, fmt, *args):  # keep server quiet
        pass

def _start_gateway(port: int):
    srv = socketserver.TCPServer(("127.0.0.1", port), _Handler)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    return srv, t

def main() -> int:
    log("05 - iOS HTTP bridge ping (Python)")

    url = os.environ.get("PAXECT_IOS_URL", "http://127.0.0.1:8765")
    start_gateway = os.environ.get("PAXECT_START_GATEWAY", "0") == "1"
    payload = b"PAXECT-iOS-bridge-smoke"

    srv = None
    if start_gateway:
        try:
            srv, _ = _start_gateway(8765)
            log("started internal test gateway on :8765")
        except Exception as e:
            log(f"note: failed to start internal gateway (soft): {e}")

    try:
        req = Request(url, data=payload, method="POST", headers={"Content-Type": "application/octet-stream"})
        with urlopen(req, timeout=3) as resp:
            body = resp.read()
            try:
                j = json.loads(body.decode("utf-8", errors="replace"))
                log(f"reply ok={j.get('ok')} sha256={j.get('sha256')} len={j.get('len')}")
            except Exception:
                log("reply was not JSON (soft)")
    except (HTTPError, URLError, TimeoutError, ConnectionError, Exception) as e:
        log(f"bridge not reachable (soft): {e}")

    if srv is not None:
        try:
            srv.shutdown(); srv.server_close()
            log("stopped internal test gateway")
        except Exception:
            pass

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr); sys.exit(3)
