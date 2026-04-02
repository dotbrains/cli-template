.PHONY: build test lint install clean dev typecheck

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
MYPY := $(VENV)/bin/mypy

# Default target
.DEFAULT_GOAL := build

$(VENV)/bin/activate:
	python3 -m venv $(VENV)
	$(PIP) install -e ".[dev]"

dev: $(VENV)/bin/activate

build: dev
	$(PYTHON) -m build

test: dev
	$(PYTEST) --cov=__PROJECT_NAME__ --cov-report=term-missing --cov-fail-under=80

typecheck: dev
	$(MYPY) src/

lint: dev
	$(RUFF) check src/ tests/
	$(RUFF) format --check src/ tests/

fmt: dev
	$(RUFF) check --fix src/ tests/
	$(RUFF) format src/ tests/

install: dev
	$(PIP) install .

clean:
	rm -rf $(VENV) dist/ build/ *.egg-info src/*.egg-info .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
