.PHONY: install verify test clean

VENV_PATH := $(shell poetry env info -p)
PYTHON := $(VENV_PATH)/bin/python

install:
	@echo "--- Installing dependencies ---"
	poetry install --with dev

verify: install
	@echo "--- Running VaultGhost Verification ---"
	@$(PYTHON) tools/verify_run.py

test: install
	@echo "--- Running Test Suite ---"
	@$(PYTHON) -m pytest tests/

clean:
	@echo "--- Cleaning up ---"
	@rm -rf .venv .pytest_cache __pycache__
