.PHONY: install verify test clean

VENV_PATH := $(shell poetry env info -p)
PYTHON := $(VENV_PATH)/bin/python

install:
	@echo "--- Installing dependencies ---"
	poetry install --with dev --no-root

verify: install
	@echo "--- Running VaultGhost Verification ---"
	@$(PYTHON) tools/verify_run.py

test: install
	@echo "--- Running Test Suite ---"
	@$(PYTHON) -m pytest -q tests/

verify-tampered: install
	@echo "--- Running Tampered Verification Test ---"
	@$(PYTHON) tools/verify_tamper.py/

clean:
	@echo "--- Cleaning up ---"
	@rm -rf .venv .pytest_cache __pycache__ .github/workflows/__pycache__ tests/__pycache__ tools/__pycache__
