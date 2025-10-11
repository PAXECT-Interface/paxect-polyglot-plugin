cd ~/paxect-suite/paxect-polyglot-plugin

cat > README.md <<'EOF'
# PAXECT Polyglot Plugin

> Plug-and-play. Cross-OS. Deterministic (SHA-256). No telemetry.

## Quick Start

**Step 1 — Get it**
    git clone https://github.com/PAXECT-Interface/paxect-polyglot-plugin.git
    cd paxect-polyglot-plugin/plugins/polyglot

**Step 2 — Try a tiny demo (10s)**
    python3 ./00_env_smoke.py
_Expect: prints a SHA-256 and ends with **OK**._

**Step 3 — Run 3 key demos (≈1 min)**
    python3 ./01_packaging_provenance.py && \
    python3 ./02-core-integration.py && \
    python3 ./03_universal_smoke.py

**Step 4 — Use in practice (no Core required)**
    python3 ./paxect_polyglot_plugin.py
_Result: deterministic output (SHA-256) and **OK** on Windows / macOS / Linux (Python 3)._

> Windows tip: if `python3` isn’t found, use `py <script>.py`.

---

## Demos (one-liners)
- **00 – Environment smoke** → temp write + SHA-256; soft launcher; **OK**
- **01 – Packaging & Provenance** → tiny file + SHA-256; soft launcher; **OK**
- **02 – Core integration (Python)** → small scaffold; soft launcher; **OK**
- **03 – Universal smoke** → OS/arch + tool presence (bash/adb/pwsh/zsh); **OK**
- **04 – Android ADB smoke** → ADB/device soft check; **OK** even if missing
- **05 – iOS HTTP bridge ping** → POST to `127.0.0.1:8765`; soft if unreachable; **OK**
- **06 – Toolchain inventory** → versions or “missing (soft)”; **OK**
- **07 – 5-in-1 smoke** → file, launcher, bash, ADB, iOS-ping (all soft); **OK**

> Note: “launcher missing (soft)” is informational — not an error.

---

## Friendly Troubleshooting (30s)
- **`python3: not found`** → Use `py` (Windows) or install Python 3.
- **ADB/iOS ping missing** → That’s fine; demos still end with **OK**.
- **Permission denied** → Run from your user folder; avoid `sudo`.
- **Weird output?** → Paste your console log in an issue.
- **Offline?** → All demos run offline; no network required.
EOF
