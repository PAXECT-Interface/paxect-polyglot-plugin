#!/usr/bin/env python3
# Demo 04 - Android ADB smoke (Python, cross-OS)
# Goal: soft-check ADB and (if present) do a tiny on-device test; always end with OK.

import sys, time, shutil, subprocess

def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

def has_cmd(name: str) -> bool:
    return shutil.which(name) is not None

def run(cmd):
    try:
        p = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()
    except Exception as e:
        return 127, "", str(e)

def main() -> int:
    log("04 - Android ADB smoke (Python)")

    # 1) ADB present? (soft)
    if not has_cmd("adb"):
        log("adb not found (not fatal for demo 04).")
        log("OK"); return 0

    # 2) Any device online? (soft)
    rc, _, _ = run(["adb", "get-state"])
    if rc != 0:
        log("no Android device online (not fatal for demo 04).")
        log("OK"); return 0

    # 3) Tiny on-device smoke (soft)
    _, serial, _ = run(["adb", "get-serialno"])
    log(f"device={serial or 'unknown'}")

    # Write a small test file (soft)
    run(["adb", "shell", "echo PAXECT-Polyglot > /sdcard/paxect_smoke.txt"])
    # Verify presence (soft)
    run(["adb", "shell", "ls -l /sdcard/paxect_smoke.txt"])

    log("OK")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"ERR: {e}", file=sys.stderr); sys.exit(3)
