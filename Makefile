.PHONY: install install-deps test clear

PYTHON := python3
PIP := $(PYTHON) -m pip

default: install test clear

# Target to install dependencies
install-deps:
	$(PIP) install -r requirements.txt

# Target to run tests
install:
	pip install .

# Target to test RestAPI V1
test:
	$(PYTHON) -m pytest tests/test_*.py -xv

clear:
	rm *.mp4 *.webm *.mkv *.m4a *.part *.opus *.ytdl
