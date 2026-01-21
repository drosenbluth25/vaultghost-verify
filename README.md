# VaultGhost Minimal Verification Pipeline

This repository provides a **minimal, reproducible, and deterministic** pipeline for verifying a VaultGhost run manifest. It adheres to strict constraints for verification, ensuring that the output is byte-for-byte stable across different environments.

## Public Repo Purpose

The primary purpose of this repository is to serve as a **reproducible test vector** for VaultGhost verification. It demonstrates the core principles of hash chain validation and receipt matching with a single, simple command.

## Hard Constraints Adherence

1.  **Deterministic Outputs:** The verification script (`tools/verify_run.py`) prints a fixed, human-readable report that is guaranteed to match `EXPECTED_OUTPUT.txt`.
2.  **Pinned Dependencies:** Dependencies are managed and pinned using `pyproject.toml` and `poetry.lock`.
3.  **One Command Verification:** The entire verification process is executed via `make verify`.
4.  **No Hidden Network Calls:** The verification script is a pure Python script with no external dependencies beyond the standard library and the pinned dependencies.
5.  **Expected Output:** The script's output is checked against `EXPECTED_OUTPUT.txt` and exits with code `0` on success.

## Setup Steps

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone <REPO_URL>
    cd vaultghost-verify
    ```

2.  **Install Poetry (if not already installed):**
    ```bash
    pip install poetry
    ```

3.  **Install dependencies and create virtual environment:**
    ```bash
    make install
    ```

## Verification

### Exact Verify Command

The verification is executed using a single `make` command.

```bash
make verify
```

### Expected Output Snippet

The command will print the following output exactly, which is also stored in `EXPECTED_OUTPUT.txt`:

```text
VaultGhost Verification Report
==============================
Run ID: vg-run-2026-01-21-001
Status: VERIFIED
Steps Validated: 2
Hash Chain: OK
Receipt Match: OK
Final Hash: 6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b
```

If the output does not match this exactly, the `make verify` command will still succeed (as the script exits 0), but the CI/test suite (`make test`) will fail, as it checks for byte-for-byte equivalence.

## Acceptance Criteria

-   **Fresh clone + install + one command => identical output:** Ensured by pinned dependencies and the `test_deterministic_output` test case.
-   **Artifact modification failure:** Ensured by the `test_failure_on_tamper` test case, which verifies that a tampered manifest results in a non-zero exit code and a clear discrepancy message.
