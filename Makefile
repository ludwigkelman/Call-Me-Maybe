PYTHON := python3
VENV := .venv
BIN := $(VENV)/bin
MAIN := filename.py
CONFIG := config.txt

.PHONY: install run debug clean lint lint-strict

$(VENV):
	$(PYTHON) -m venv $(VENV)

install: $(VENV)
	$(BIN)/python -m pip install --upgrade pip
	$(BIN)/python -m pip install flake8 mypy

run: install
	$(BIN)/python $(MAIN) $(CONFIG)

debug: install
	$(BIN)/python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	rm -rf $(VENV)

lint: install
	$(BIN)/flake8 .
	$(BIN)/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(BIN)/flake8 .
	$(BIN)/mypy . --strict
