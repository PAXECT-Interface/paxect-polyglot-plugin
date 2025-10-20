#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""
Demo 11 — PAXECT Polyglot Fail & Self-Recover
Simulates a UTF-8 decoding failure, then verifies deterministic recovery.
"""

import subprocess, tempfile
from pathlib import Path

TMP = Path(tempfile.gettempdir()) / "paxect_demo11_polyglot"
TMP.mkdir(exist_ok=True)
BAD = TMP / "bad_utf8.txt"
GOOD = TMP / "good_utf8.txt"
OUT = TMP / "out.txt"
LOG = TMP / "polyglot_recover.log"

BAD.write_bytes(b"good line\n" + b"\xff\xfe\xfa" + b"\nend\n")
GOOD.write_text("polyglot recovery works\n", encoding="utf-8")

def run_polyglot(mode, infile, outfile):
    r = subprocess.run(
        ["python3", "paxect_polyglot_plugin.py", "--mode", mode,
         "--input", str(infile), "--output", str(outfile)],
        capture_output=True, text=True)
    return r.returncode, r.stderr.strip()

print("=== Demo 11 — PAXECT Polyglot Fail & Self-Recover ===")
print("[*] Step 1: Decode corrupted UTF-8 (expect fail)")
code, err = run_polyglot("upper", BAD, OUT)
print(f"   returncode: {code}")
if err: print(f"   error: {err}")

print("[*] Step 2: Decode valid UTF-8 (expect recovery)")
code2, err2 = run_polyglot("upper", GOOD, OUT)
if code2 == 0:
    print(f"[+] Recovery OK — output: {OUT.read_text().strip()}")
    print("✅ Self-recovery confirmed.")
else:
    print(f"[!] Recovery failed: {err2}")

with open(LOG, "w", encoding="utf-8") as f:
    f.write(f"bad_code={code}, err={err}\n")
    f.write(f"good_code={code2}, err={err2}\n")

print(f"[log] {LOG}")
