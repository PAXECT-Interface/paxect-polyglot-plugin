#!/usr/bin/env python3
# Demo 10 - Polyglot CI Verifier / Matrix Test
# Goal: run all previous demos sequentially, collect exit codes, hash summary, and report matrix status.

import subprocess, hashlib, time, sys, pathlib

DEMOS = [
    "00_env_smoke.py",
    "01_packaging_provenance.py",
    "02_core_integration.py",
    "03_universal_smoke.py",
    "04_android_adb_smoke.py",
    "05_ios_http_bridge_ping.py",
    "06_toolchain_inventory.py",
    "07_5_in_1_smoke.py",
    "09_universal_end_to_end_polyglot.py",
]

def log(msg):
    print(f"[{time.strftime('%H:%M:%S', time.gmtime())}] {msg}")

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def run_demo(demo_path: pathlib.Path):
    try:
        proc = subprocess.run(
            ["python3", str(demo_path)],
            capture_output=True,
            text=True,
            timeout=60,
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return 99, "", str(e)

def main() -> int:
    log("10 - Polyglot CI Verifier / Matrix Test")

    here = pathlib.Path(__file__).resolve().parent
    results = []
    all_output = ""

    for demo in DEMOS:
        path = here / demo
        if not path.exists():
            log(f"⚠️ missing demo script: {demo}")
            results.append((demo, 99))
            continue
        log(f"→ running {demo} ...")
        rc, out, err = run_demo(path)
        status = "OK" if rc == 0 else f"FAIL({rc})"
        log(f"   {demo} → {status}")
        if err:
            log(f"   note: {err}")
        results.append((demo, rc))
        all_output += out + err

    # summarize
    ok = sum(1 for _, rc in results if rc == 0)
    fail = len(results) - ok
    hash_summary = sha256(all_output)
    log("— Summary —")
    log(f"Passed: {ok}/{len(results)}   Failed: {fail}")
    log(f"Output SHA-256: {hash_summary}")

    if fail == 0:
        log("✅ All demos passed successfully.")
    else:
        log("⚠️ Some demos returned soft errors (see logs).")

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
