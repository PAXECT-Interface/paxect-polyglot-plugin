#!/usr/bin/env python3
# Demo 00 - Environment smoke (Python, cross-OS)
import sys, os, time, tempfile, pathlib, hashlib, platform, subprocess

def log(m): print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {m}")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1<<20), b""): h.update(b)
    return h.hexdigest()

def main():
    log("00 - Environment smoke (Python)")
    log(f"python={sys.version.split()[0]} os={platform.system()} arch={platform.machine()}")

    # temp write + hash (soft)
    try:
        tmp = pathlib.Path(tempfile.mkdtemp())
        f = tmp / "env_smoke.txt"
        f.write_bytes(b"PAXECT Polyglot - env smoke\n")
        log(f"temp_file={f}")
        log(f"sha256={sha256(f)}")
    except Exception as e:
        log(f"note: temp write/read issue (soft): {e}")

    # optional launcher (soft)
    here = pathlib.Path(__file__).resolve().parent
    plugins_dir = (here / ".." / "..").resolve()
    launcher = plugins_dir / "paxect-polyglot-plugin.sh"
    if launcher.exists() and os.access(launcher, os.X_OK):
        log(f"launcher OK: {launcher}")
        try:
            subprocess.run(["/bin/bash", str(launcher), "--version"],
                           check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass
    else:
        log(f"launcher missing (not fatal for demo 00): {launcher}")

    log("OK"); return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except KeyboardInterrupt: sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr); sys.exit(3)
