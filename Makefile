# Makefile - single entrypoint for the gate suite (mirrors .github/workflows/ci.yml)
VENV ?= .venv
PY   := $(VENV)/bin/python
PIP  := $(VENV)/bin/pip

.PHONY: bootstrap lint format-check test test-cov security suppressions drift-guard all clean

bootstrap:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e '.[dev]'

lint:
	$(VENV)/bin/ruff check .

format-check:
	$(VENV)/bin/black --check .

test:
	$(PY) -m pytest tests/ -q

test-cov:
	$(PY) -m pytest tests/ -q --cov=src --cov=app --cov=config --cov-report=term --cov-fail-under=35

security:
	$(VENV)/bin/pip-audit --progress-spinner off

suppressions:
	$(PY) scripts/audit_suppressions.py --check

drift-guard: test
	git diff --exit-code

all: lint format-check suppressions security test-cov drift-guard

clean:
	rm -rf $(VENV) .pytest_cache .coverage
