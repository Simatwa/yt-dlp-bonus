.PHONY: install install-deps test

PYTHON := python3
PIP := $(PYTHON) -m pip

default: install

# Target to install dependencies
install-deps:
	$(PIP) install -r requirements.txt

# Target to run tests
install:
	pip install -e . --use-pep517

# Target to test RestAPI V1
test:
	$(PYTHON) -m pytest tests/test_*.py -xv