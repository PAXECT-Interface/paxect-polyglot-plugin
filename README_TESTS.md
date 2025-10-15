
# 🧠 PAXECT Polyglot Plugin — Test & Quality Validation

This document provides a detailed overview of the testing, verification,  
and coverage framework for the **PAXECT Polyglot Plugin** — the  
cross-language bridge connecting PAXECT Core with external runtimes.

---

## 1. Overview

The Polyglot Plugin is validated through a deterministic test suite that ensures:

- ✅ **Bit-identical** encode/decode behavior across languages  
- ✅ **Cross-OS and cross-runtime** consistency  
- ✅ **Provenance verification** for build and packaging  
- ✅ **Full offline test execution** (no network dependencies)  
- ✅ **Integrity validation** via SHA-256 and CRC32  

Testing and coverage are performed using:

- **pytest** — structured, deterministic test execution  
- **coverage.py** — detailed code-path and branch analysis  
- **zstandard**, **psutil**, and **subprocess** — runtime and bridge validation  

---

## 2. Repository Structure

```

paxect-polyglot-plugin/
├── paxect_polyglot_plugin.py          # Core bridge module
├── tests/                             # Test suite
│   ├── test_bridge_integrity.py
│   ├── test_cross_language_io.py
│   ├── test_toolchain_scan.py
│   ├── test_core_integration.py
│   ├── test_packaging_provenance.py
│   ├── test_stream_consistency.py
│   └── test_universal_smoke.py
├── coverage_run.sh                    # Unified coverage runner
├── pytest.ini                         # Pytest configuration
└── README_TESTS.md                    # This document

````

---

## 3. Environment Setup

```bash
# Clone the repository
git clone https://github.com/<your-org>/paxect-polyglot-plugin.git
cd paxect-polyglot-plugin

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt
````

Optional:

```bash
python3 -m pip install numpy
sudo apt install nodejs golang
```

---

## 4. Running Tests

Run all tests with coverage reporting:

```bash
./coverage_run.sh
```

Or manually:

```bash
python3 -m coverage run -m pytest -v
python3 -m coverage report -m
```

This suite validates:

* Cross-language roundtrip consistency
* Deterministic CLI bridge communication
* Toolchain discovery and provenance tracking
* Multi-platform encoding and decoding correctness

---

## 5. Example Output

```
=== PAXECT Polyglot Plugin — Test Suite ===
→ Running deterministic bridge validation...
→ Running Core integration check...
→ Verifying Node.js and Go subprocess bridges...
✅ All tests passed (12/12)
✅ Cross-language hash integrity verified.
Coverage: 94%
```

---

## 6. Test Metrics (Reference)

| Metric         | Result (Reference)      |
| -------------- | ----------------------- |
| Tests Passed   | 100% (12 / 12)          |
| Coverage       | 94%                     |
| Framework      | pytest + coverage.py    |
| Compatibility  | Linux · macOS · Windows |
| Python Version | 3.9 – 3.12              |

---

## 7. CI/CD Integration

Fully compatible with GitHub Actions, GitLab CI, Jenkins, and Bamboo.

**Example workflow (GitHub Actions):**

```yaml
- name: Run tests
  run: |
    chmod +x coverage_run.sh
    ./coverage_run.sh
```

Artifacts such as `.coverage`, `__pycache__/`, and `.pytest_cache/` are automatically excluded in `.gitignore`.

---

## 8. Coverage Script (`coverage_run.sh`)

```bash
#!/usr/bin/env bash
# PAXECT Polyglot Plugin — Coverage Runner

set -e
echo "=== PAXECT Polyglot Plugin — Test Suite ==="
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
echo "Started: $DATE"
echo

rm -f .coverage || true
rm -rf htmlcov || true

python3 -m coverage run -m pytest -v --maxfail=1 --disable-warnings
python3 -m coverage report -m
python3 -m coverage html

echo
echo "✅ HTML coverage report generated at: htmlcov/index.html"
echo "=== Test run completed successfully ==="
```

Make the script executable:

```bash
chmod +x coverage_run.sh
```

---

## 9. Quality Principles

* **Reproducibility:** Identical results across OSes and runtimes
* **Integrity:** CRC32 + SHA-256 verification on all bridges
* **Isolation:** No network or cloud dependencies
* **Transparency:** CLI logs and per-run validation hashes
* **Stability:** Predictable, deterministic runtime behavior

---

## 10. License

Released under the **Apache 2.0 License**
© 2025 PAXECT Systems. All rights reserved.

---

> 🧩 *PAXECT Polyglot — validated across systems, languages, and time.*


```
