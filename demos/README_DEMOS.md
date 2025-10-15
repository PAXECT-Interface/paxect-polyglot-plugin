

---

# 🧪 **PAXECT Polyglot Plugin — Test & Quality Validation**

This document describes the full testing and validation framework for the
**PAXECT Polyglot Plugin**, ensuring cross-language integrity, reproducibility, and safe interoperability across all supported platforms.

---

## 1️⃣ **Overview**

The Polyglot Plugin is validated through a deterministic test suite designed to guarantee:

* Stable cross-language data exchange between **Python**, **Node.js**, and **Go**
* Bit-identical reproducibility under all operating systems
* Safe failover for missing interpreters or compilers
* Complete offline verification (no external network dependencies)

Testing and coverage are performed using:

* **pytest** — structured functional and integration testing
* **coverage.py** — branch and statement coverage reporting
* **hashlib** — SHA-256 validation between language bridges
* **subprocess** — language-agnostic interprocess I/O verification

---

## 2️⃣ **Repository Structure**

```bash
paxect-polyglot-plugin/
├── paxect_polyglot_plugin.py         # Standalone CLI module
├── tests/                            # Polyglot validation suite
│   ├── test_cross_language_bridge.py
│   ├── test_utf8_transform.py
│   ├── test_io_integrity.py
│   ├── test_process_fail_safe.py
│   ├── test_cli_modes.py
│   └── ...
├── coverage_run.sh                   # Coverage test runner script
├── pytest.ini                        # Pytest configuration (see below)
└── README_TESTS.md                   # This document
```

---

## 3️⃣ **Environment Setup**

```bash
# Clone the repository
git clone https://github.com/<your-org>/paxect-polyglot-plugin.git
cd paxect-polyglot-plugin

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt
```

Optional (for cross-language tests):

```bash
sudo apt install nodejs golang-go -y
```

---

## 4️⃣ **Running Tests**

To run the full test suite with coverage reporting:

```bash
./coverage_run.sh
```

or manually:

```bash
python3 -m coverage run -m pytest -v
python3 -m coverage report -m
```

This executes all bridge validation tests, CLI mode checks, and UTF-8 transformations.

---

## 5️⃣ **Test Metrics (Reference)**

| Metric        | Result (Reference)      |
| ------------- | ----------------------- |
| Tests Passed  | 100 % (10 / 10)         |
| Coverage      | 93 %                    |
| Framework     | pytest + coverage.py    |
| Compatibility | Linux · macOS · Windows |
| Python        | 3.9 – 3.12              |

---

## 6️⃣ **Test Modules**

| Module                          | Description                                                  |
| ------------------------------- | ------------------------------------------------------------ |
| `test_cross_language_bridge.py` | Ensures correct Python ↔ Node ↔ Go communication.            |
| `test_utf8_transform.py`        | Verifies upper/lowercase UTF-8 conversions (strict mode).    |
| `test_io_integrity.py`          | Checks stdin/stdout byte parity and hash integrity.          |
| `test_process_fail_safe.py`     | Simulates absent runtimes and ensures safe degradation.      |
| `test_cli_modes.py`             | Validates CLI `--mode` operations (health/test/upper/lower). |

---

## 7️⃣ **Pytest Configuration (`pytest.ini`)**

```ini
[pytest]
minversion = 7.0
addopts = -ra -q
testpaths = tests
python_files = test_*.py
filterwarnings =
    ignore::DeprecationWarning
```

This ensures consistent test discovery and stable execution across all environments.

---

## 8️⃣ **Coverage Script (`coverage_run.sh`)**

```bash
#!/usr/bin/env bash
# PAXECT Polyglot Plugin — Coverage Runner

set -e
echo "=== PAXECT Polyglot Plugin — Coverage Test Run ==="
DATE=$(date -u +"%Y-%m-%d %H:%M:%S UTC")
echo "Started: $DATE"
echo

rm -f .coverage || true
rm -rf htmlcov || true

python3 -m coverage run -m pytest -v --maxfail=1 --disable-warnings
python3 -m coverage report -m
python3 -m coverage html

echo
echo "HTML report available at: htmlcov/index.html"
echo "=== Test run completed successfully ==="
```

Make it executable:

```bash
chmod +x coverage_run.sh
```

---

## 9️⃣ **CI/CD Integration**

Fully compatible with enterprise CI frameworks:

* **GitHub Actions:** Add a step for `./coverage_run.sh`
* **GitLab CI:** Include a `pytest` job with artifact uploads
* **Jenkins / Bamboo:** Run inside isolated `.venv` environments

Example for **GitHub Actions**:

```yaml
jobs:
  test-polyglot:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Run coverage tests
        run: ./coverage_run.sh
```

---

## 🔒 **Quality Principles**

| Principle           | Description                                                    |
| ------------------- | -------------------------------------------------------------- |
| **Reproducibility** | Every bridge operation produces identical outputs across OSes. |
| **Safety**          | No permanent file writes or remote calls.                      |
| **Isolation**       | Tests run fully offline and clean up temporary files.          |
| **Transparency**    | All results logged with timestamps and hash verification.      |

---

## 🪪 **License**

All test utilities and validation scripts are released under the same license as the Polyglot engine:
**Apache 2.0 License** — © 2025 PAXECT Systems. All rights reserved.

---

