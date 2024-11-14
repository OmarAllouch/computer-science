PYTHON = python3
PIP = $(PYTHON) -m pip

.DEFAULT_GOAL := install

.PHONY: install
install:
	@echo "Installing easy-git-cli..."
	$(PIP) install --upgrade pip
	$(PIP) install easy-git-cli

.PHONY: run-help
run: install
	@echo "Running easy-git --help..."
	easy-git --help

.PHONY: help
help:
	@echo "Makefile Usage:"
	@echo "  make              - Install easy-git-cli (default)"
	@echo "  make run-help     - Run easy-git --help"
	@echo "  make help         - Show this help message"
