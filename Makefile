.PHONY: help clean install install-dev lint lint-check type-check check all

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
BLACK := $(VENV)/bin/black
ISORT := $(VENV)/bin/isort
MYPY := $(VENV)/bin/mypy

help:
	@echo "Available commands:"
	@echo "  make clean            - Remove temporary files and caches"
	@echo "  make install          - Install production dependencies"
	@echo "  make install-dev      - Install development dependencies"
	@echo "  make .venv		       - Creates the virtual env in .venv/ dir"
	@echo "  make lint         	   - Format code with Black and Isort"
	@echo "  make lint-check       - Run linting checks (Isort and Black in check mode)"
	@echo "  make type-check       - Run type checking with Mypy"
	@echo "  make check            - Run all checks (lint + type-check)"
	@echo "  make all              - Clean, format, and run all checks"

clean:
	@echo "Cleaning temporary files and caches..."
	find . -path "./$(VENV)" -prune -o -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -path "./$(VENV)" -prune -o -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -path "./$(VENV)" -prune -o -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -path "./$(VENV)" -prune -o -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -path "./$(VENV)" -prune -o -type d -name ".tox" -exec rm -rf {} + 2>/dev/null || true
	find . -path "./$(VENV)" -prune -o -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -path "./$(VENV)" -prune -o -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	find . -path "./$(VENV)" -prune -o -type f -name "*.pyc" -delete
	find . -path "./$(VENV)" -prune -o -type f -name "*.pyo" -delete
	find . -path "./$(VENV)" -prune -o -type f -name "*.pyd" -delete
	find . -path "./$(VENV)" -prune -o -type f -name ".coverage" -delete
	find . -path "./$(VENV)" -prune -o -type d -name ".coverage*" -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete!"

install: venv
	@echo "Installing production dependencies..."
	$(PYTHON) -m pip install -e .

install-dev: venv
	@echo "Installing development dependencies..."
	$(PYTHON) -m pip install -e ".[dev]"

venv:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)
	@echo "Bootstrapping pip..."
	$(PYTHON) -m ensurepip --upgrade || true
	$(PYTHON) -m pip install --upgrade pip setuptools wheel

lint: install-dev
	@echo "Running Black formatter..."
	$(BLACK) .
	@echo "Running Isort import sorter..."
	$(ISORT) .
	@echo "Formatting complete!"

lint-check: install-dev
	@echo "Running Isort check..."
	$(ISORT) --check-only --diff .
	@echo "Running Black check..."
	$(BLACK) --check --diff .

type-check: install-dev
	@echo "Running Mypy type checker..."
	$(MYPY) .

check: lint-check type-check
	@echo "All checks passed!"

all: clean lint type-check
	@echo "All tasks completed!"
