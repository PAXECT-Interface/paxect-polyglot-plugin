<p align="center">
  <img src="ChatGPT%20Image%202%20okt%202025%2C%2022_33_51.png" alt="PAXECT logo" width="200"/>
</p>

---

#  Contributing Guidelines

Thank you for your interest in contributing to the **PAXECT Polyglot Plugin**.

---

##  Overview

This repository is part of the **PAXECT Interface Ecosystem**.
All contributions must remain:

* **Deterministic:** no randomization or non-reproducible behavior
* **Cross-language:** compatible with the Polyglot bridge (Python, Node.js, Go, etc.)
* **Platform-agnostic:** must run on Linux, macOS, and Windows
* **Dependency-free:** no cloud calls or AI/ML frameworks allowed
* **Secure:** respect PAXECT Core’s privacy-by-default policy

Each change must preserve **byte-identical behavior** and remain consistent across all supported runtimes.

---

##  Development Setup

1. **Fork this repository** on GitHub
   Create your own fork to contribute safely.

2. **Clone your fork locally**

   ```bash
   git clone https://github.com/<your-username>/paxect-polyglot-plugin.git
   cd paxect-polyglot-plugin
   ```

3. **(Optional) Create and activate a virtual environment**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Install dependencies**

   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. **Run basic verification**

   ```bash
   python3 demos/00_env_smoke.py
   ```

---

##  Testing Standards

* Use **pytest** for all new tests (`tests/` directory)
* Keep tests **deterministic and platform-neutral**
* Validate both **stdin/stdout** and **file-based** behavior
* Avoid hardcoded paths — use `tempfile` for all test data

Example:

```bash
python3 -m pytest -v
```

---

##  Pull Requests

* Follow the naming pattern:
  `feature/<short-description>` or `fix/<issue-id>`
* Add a clear description and link to related issues
* Ensure all demos still pass (`python3 demos/10_polyglot_ci_verifier.py`)
* Code must pass static linting (flake8, black)

---

##  Security and Compliance

* Do not add third-party telemetry, analytics, or network dependencies
* Avoid AI-generated randomness, pseudo-learning, or heuristic behavior
* Each PR is automatically reviewed for deterministic compliance

---

##  Communication

* **Issues:** Bug reports, feature ideas, reproducibility feedback
* **Discussions:** Technical proposals or architecture debates
* **Security:** Please report privately to `security@paxect-team@outlook.com`

---

##  License

All contributions fall under the **Apache 2.0 License** and
are subject to PAXECT’s deterministic and audit-compliance policies.

---


