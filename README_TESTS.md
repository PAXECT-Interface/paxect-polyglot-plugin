

# 🧪 **PAXECT Polyglot Plugin — Test and Quality Validation**

This document provides a detailed overview of the testing, coverage, and validation framework for the
**PAXECT Polyglot Plugin** — the deterministic multi-language bridge of the PAXECT ecosystem.

---

## 1. Overview

The Polyglot Plugin is validated through a comprehensive test suite designed to ensure:

* Deterministic runtime and reproducible transformations
* Stable cross-language bridge behavior (Python, Node.js, Go)
* Cross-platform consistency (Linux, macOS, Windows)
* Full offline operation with no network dependencies

Testing and coverage are performed using:

* **pytest** — structured functional and integration testing
* **coverage.py** — detailed code-path and branch coverage reports
* **zstandard**, **hashlib**, and **subprocess** for runtime bridge checks

---

## 2. Repository Structure

```
paxect-polyglot-plugin/
├── paxect_polyglot_plugin.py     # Main CLI and I/O logic
├── tests/                        # Automated validation suite
│   ├── test_bridge_roundtrip.py
│   ├── test_encoding_utf8.py
│   ├── test_error_handling.py
│   ├── test_multilang_cli.py
│   └── test_reproducibility.py
├── coverage_run.sh               # Script to execute full coverage tests
├── pytest.ini                    # Pytest configuration
└── README_TESTS.md               # This document
```

---

## 3. Environment Setup

```bash
# Clone repository
git clone https://github.com/<your-org>/paxect-polyglot-plugin.git
cd paxect-polyglot-plugin

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt
```

Optional (for extended coverage):

```bash
python3 -m pip install pytest coverage numpy
```

---

## 4. Running Tests

### Run the entire test suite:

```bash
python3 -m pytest -v
```

### Run with coverage:

```bash
python3 -m coverage run -m pytest -v
python3 -m coverage report -m
```

### Generate an HTML report:

```bash
python3 -m coverage html
```

---

## 5. Example `pytest.ini`

```ini
# pytest.ini — PAXECT Polyglot standard configuration
[pytest]
addopts = -ra -q
testpaths = tests
python_files = test_*.py
python_functions = test_*
filterwarnings =
    ignore::DeprecationWarning
```

---

## 6. Coverage Script (`coverage_run.sh`)

```bash
#!/usr/bin/env bash
# PAXECT Polyglot — Coverage Runner

set -e
echo "=== PAXECT Polyglot — Coverage Test Run ==="
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
echo "Started: $DATE"
echo

rm -f .coverage || true
rm -rf htmlcov || true

python3 -m coverage run -m pytest -v --maxfail=1 --disable-warnings
python3 -m coverage report -m
python3 -m coverage html

echo
echo "HTML report generated at: htmlcov/index.html"
echo "=== Test run completed successfully ==="
```

Make it executable:

```bash
chmod +x coverage_run.sh
```

---

## 7. Test Metrics (Reference)

| Metric        | Result                |
| ------------- | --------------------- |
| Tests Passed  | 100 % (11/11)         |
| Coverage      | 95 % (core bridge)    |
| Framework     | pytest + coverage.py  |
| Compatibility | Linux, macOS, Windows |
| Python        | 3.9 – 3.12            |

---

## 8. CI/CD Integration

### GitHub Actions Example

```yaml
jobs:
  polyglot-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Run Polyglot Tests
        run: ./coverage_run.sh
```

### GitLab CI Example

```yaml
polyglot_test:
  image: python:3.12
  script:
    - ./coverage_run.sh
  artifacts:
    when: always
    paths:
      - htmlcov/
```

---

## 9. Quality Principles

* **Reproducibility:** Identical cross-language results across OSes
* **Integrity:** Verified data path with CRC32 + SHA-256
* **Isolation:** No external I/O or network required
* **Transparency:** Deterministic runtime and inspectable logs
* **Stability:** Predictable bridge latency under load

---

## 10. License

All test utilities and scripts are released under the same license as the core engine:
**Apache 2.0 License** — © 2025 PAXECT Systems. All rights reserved.

---




```
