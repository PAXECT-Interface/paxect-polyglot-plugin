#!/usr/bin/env python3
# Demo 03 - Universal smoke (Python)
# Goal: quiet cross-OS sanity check; always ends with OK.

import sys, os, time, platform, tempfile, pathlib, hashlib, shutil, subprocess

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

def sha256(p: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def has_cmd(name: str) -> bool:
    return shutil.which(name) is not None

def main() -> int:
    log("03 - Universal smoke (Python)")
    log(f"python={sys.version.split()[0]} os={platform.system()} arch={platform.machine()}")

    # Temp write + hash (soft)
    try:
        tmp = pathlib.Path(tempfile.mkdtemp())
        f = tmp / "universal_smoke.txt"
        f.write_bytes(b"PAXECT Polyglot - demo 03\n")
        log(f"temp_file={f}")
        log(f"sha256={sha256(f)}")
    except Exception as e:
        log(f"note: temp write/read issue (soft): {e}")

    # Optional tools (soft)
    for tool in ["bash", "adb", "pwsh", "zsh"]:
        log(f"tool {tool}: {'OK' if has_cmd(tool) else 'missing (soft)'}")

    # Optional launcher (soft)
    here = pathlib.Path(__file__).resolve().parent
    plugins_dir = (here / ".." / "..").resolve()
    launcher = plugins_dir / "paxect-polyglot-plugin.sh"
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
        log(f"launcher missing (soft): {launcher}")

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr); sys.exit(3)
