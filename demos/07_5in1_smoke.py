#!/usr/bin/env python3
# Demo 07 - 5-in-1 smoke (Python, cross-OS)
# Checks (all soft): A) file I/O + SHA-256, B) launcher presence, C) bash presence,
# D) Android ADB presence/device, E) iOS HTTP bridge ping to 127.0.0.1:8765. Always ends with OK.

import sys, os, time, pathlib, tempfile, hashlib, shutil, subprocess, json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def has_cmd(name: str) -> bool:
    return shutil.which(name) is not None

def run(cmd):
    try:
        p = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:
        return 127, "", str(e)

def main() -> int:
    log("07 - 5-in-1 smoke (Python)")

    # A) File I/O + SHA-256 (soft)
    try:
        tmp = pathlib.Path(tempfile.mkdtemp())
        f = tmp / "five_in_one.bin"
        f.write_bytes(b"PAXECT Polyglot - 5-in-1 smoke\n")
        log(f"[A] file={f}")
        log(f"[A] sha256={sha256(f)}")
    except Exception as e:
        log(f"[A] note: temp write/read issue (soft): {e}")

    # B) Launcher presence (soft)
    here = pathlib.Path(__file__).resolve().parent
    plugins_dir = (here / ".." / "..").resolve()
    launcher = plugins_dir / "paxect-polyglot-plugin.sh"
    if launcher.exists() and os.access(launcher, os.X_OK):
        log(f"[B] launcher OK: {launcher}")
        rc, _, err = run(["/bin/bash", str(launcher), "--version"])
        if rc != 0 and err:
            log(f"[B] launcher --version non-zero (soft): rc={rc} err={err}")
    else:
        log(f"[B] launcher missing (soft): {launcher}")

    # C) Bash presence (soft)
    if has_cmd("bash"):
        rc, out, err = run(["bash", "-lc", "echo polyglot-bash-ok"])
        if rc == 0:
            log("[C] bash OK")
        else:
            log(f"[C] bash check non-zero (soft): rc={rc} err={err}")
    else:
        log("[C] bash not found (soft)")

    # D) Android ADB (soft)
    if has_cmd("adb"):
        rc, _, _ = run(["adb", "get-state"])
        if rc == 0:
            rc2, serial, _ = run(["adb", "get-serialno"])
            log(f"[D] adb device serial={serial or 'unknown'}")
            run(["adb", "shell", "echo PAXECT-Polyglot > /sdcard/paxect_smoke.txt"])
            run(["adb", "shell", "ls -l /sdcard/paxect_smoke.txt"])
            log("[D] adb smoke OK (soft)")
        else:
            log("[D] no Android device online (soft)")
    else:
        log("[D] adb not found (soft)")

    # E) iOS HTTP bridge ping (soft) to localhost:8765
    url = os.environ.get("PAXECT_IOS_URL", "http://127.0.0.1:8765")
    payload = b"PAXECT-iOS-bridge-smoke"
    try:
        req = Request(url, data=payload, method="POST", headers={"Content-Type":"application/octet-stream"})
        with urlopen(req, timeout=3) as resp:
            body = resp.read()
            try:
                j = json.loads(body.decode("utf-8", errors="replace"))
                log(f"[E] reply ok={j.get('ok')} sha256={j.get('sha256')} len={j.get('len')}")
            except Exception:
                log("[E] reply was not JSON (soft)")
    except (HTTPError, URLError, TimeoutError, ConnectionError, Exception) as e:
        log(f"[E] bridge not reachable (soft): {e}")

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr); sys.exit(3)
