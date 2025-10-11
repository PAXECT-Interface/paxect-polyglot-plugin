#!/usr/bin/env python3
# Demo 02 — Core integration (Python)
# Goal: create a tiny input, print SHA-256, soft-check for launcher, end with OK.

import sys
import os
import tempfile
import hashlib
import pathlib
import subprocess
import shlex
import time

def log(msg: str) -> None:
    ts = time.strftime("%H:%M:%S", time.gmtime())
    print(f"[{ts}] {msg}")

def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    here = pathlib.Path(__file__).resolve().parent
    plugins_dir = (here / ".." / "..").resolve()
    launcher = plugins_dir / "paxect-polyglot-plugin.sh"

    log("02 - Core integration (Python)")

    # create tiny input
    tmpdir = pathlib.Path(tempfile.mkdtemp())
    inp = tmpdir / "input.bin"
    inp.write_bytes(b"PAXECT Polyglot - core integration demo\n")
    log(f"input={inp}")
    log(f"sha256={sha256(inp)}")

    # optional launcher step (not fatal if missing)
    if launcher.exists() and os.access(launcher, os.X_OK):
        log(f"launcher OK: {launcher}")
        try:
            cmd = ["/bin/bash", str(launcher), "--version"]
            subprocess.run(cmd, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    else:
        log(f"launcher missing (not fatal for demo 02): {launcher}")

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr)
        sys.exit(3)
