#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""
Demo 12 — Polyglot One-Minute Stress Test
Runs repeated upper→lower transform cycles for 60 seconds.
"""

import subprocess, tempfile, time, json
from pathlib import Path

TMP = Path(tempfile.gettempdir()) / "paxect_demo12_polyglot"
TMP.mkdir(exist_ok=True)
SRC = TMP / "source.txt"
OUT = TMP / "out.txt"
LOG = TMP / "polyglot_stress.jsonl"

SRC.write_text("paxect polyglot test data\n", encoding="utf-8")

start = time.time()
cycles, errors = 0, 0
print("=== Demo 12 — Polyglot One-Minute Stress Test ===")
print("[*] Running continuous upper→lower transform cycles for 60 seconds...")

while time.time() - start < 60:
    for mode in ("upper", "lower"):
        r = subprocess.run(
            ["python3", "paxect_polyglot_plugin.py", "--mode", mode,
             "--input", str(SRC), "--output", str(OUT)],
            capture_output=True, text=True)
        ok = r.returncode == 0
        if not ok:
            errors += 1
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "time": time.time(),
                "mode": mode,
                "returncode": r.returncode,
                "error": r.stderr.strip()
            }) + "\n")
        cycles += 1

print(f"\nCompleted cycles : {cycles}")
print(f"Errors detected  : {errors}")
print(f"Reliability     : {(1 - errors / cycles) * 100:.4f}%")
print(f"Log file        : {LOG}")

if errors == 0:
    print("✅ Polyglot engine passed 1-minute stress test without errors.")
else:
    print("⚠️ Polyglot engine reported some errors.")
