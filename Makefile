.PHONY: init \
init-venv \
update-venv \
build \
clean \
clean-build \
clean-venv \
clean-pyc \
clean-test \
test \
coverage
.DEFAULT_GOAL := help

# Python requirements
VENV ?= venv
REQUIREMENTS ?= dev-requirements.txt

# This value is true in CircleCI
# You check here: https://circleci.com/docs/2.0/env-vars/#built-in-environment-variables
CI ?= false

ifeq (false,$(CI))
# if not running in CI, we output an html report for humans
COV_REPORT := --cov-report html
else
# If running in CI we output xml report for Code Climate
COV_REPORT := --cov-report xml:coverage.xml --junitxml=test-reports/junit.xml
endif

help:
	@echo "    init"
	@echo "        Initialize development environment."
	@echo "    init-venv"
	@echo "        Initialize python environment."
	@echo "    build"
	@echo "        Builds this package."
	@echo "    clean"
	@echo "        Remove all the development environment files."
	@echo "    clean-build"
	@echo "        Remove all the build files."
	@echo "    clean-venv"
	@echo "        Remove Python virtual environment."
	@echo "    clean-pyc"
	@echo "        Remove Python artifacts."
	@echo "    clean-test"
	@echo "        Remove Test data."
	@echo "    test"
	@echo "        Run pytest."
	@echo "    coverage"
	@echo "        Generate coverage report."

init: clean init-venv init-precommit
	@echo ""
	@echo "Do not forget to activate your new virtual environment"

init-venv:
	@python3 -m venv $(VENV)
	@make update-venv

update-venv:
	@( \
		. $(VENV)/bin/activate; \
		pip install --upgrade setuptools pip; \
		pip install -r $(REQUIREMENTS); \
	)

init-precommit:
	@echo "Installing pre commit..."
	@( \
		. $(VENV)/bin/activate; \
		pre-commit install; \
	)

clean: clean-pyc clean-test clean-venv

clean-venv:
	@echo "Removing virtual environment: $(VENV)..."
	@rm -rf $(VENV)

clean-pyc:
	@echo "Removing compiled bytecode files..."
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +

clean-test: clean-pyc
	@echo "Removing previous test data..."
	@rm -rf .coverage
	@rm -rf htmlcov
	@rm -rf .pytest_cache

test: clean-test
	@( \
		. $(VENV)/bin/activate; \
		pytest; \
	)

coverage: clean-test
	@echo "Running test with coverage report..."
	@( \
		. $(VENV)/bin/activate; \
		pytest --cov --cov-report term-missing:skip-covered --no-cov-on-fail $(COV_REPORT); \
	)

clean-build:
	@echo "Removing build files"
	@rm -rf dist
	@rm -rf build
	@rm -f *.spec
	@rm -rf *.egg-info

build: clean-build
	@echo "Building package"
	@( \
		. $(VENV)/bin/activate; \
		python3 setup.py sdist; \
	)

publish: clean-build
	@echo "Building and publishing package"
	@( \
		. $(VENV)/bin/activate; \
		python3 bin/dist.py; \
		python3 setup.py sdist upload -r fury; \
	)
