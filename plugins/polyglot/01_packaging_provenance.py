#!/usr/bin/env python3
# Demo 01 - Packaging & Provenance (Python, cross-OS)
# Goal: create a tiny input, print SHA-256; soft-check launcher; end with OK.

import sys, os, tempfile, hashlib, pathlib, subprocess, time

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def main() -> int:
    here = pathlib.Path(__file__).resolve().parent
    plugins_dir = (here / ".." / "..").resolve()
    launcher = plugins_dir / "paxect-polyglot-plugin.sh"

    log("01 - Packaging & Provenance (Python)")

    # Create tiny input and print SHA-256
    td = pathlib.Path(tempfile.mkdtemp())
    inp = td / "sample.txt"
    inp.write_bytes(b"PAXECT Polyglot - provenance demo\n")
    log(f"input={inp}")
    log(f"sha256={sha256(inp)}")

    # Optional launcher (soft)
    if launcher.exists() and os.access(launcher, os.X_OK):
        log(f"launcher OK: {launcher}")
        try:
            subprocess.run(
                ["/bin/bash", str(launcher), "--version"],
                check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        except Exception:
            pass
    else:
        log(f"launcher missing (not fatal for demo 01): {launcher}")

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr); sys.exit(3)
