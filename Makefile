.PHONY: run test help

help:
	@echo "Available commands:"
	@echo "  make run   - Run the application (main.py)"
	@echo "  make test  - Run unit tests"

run:
	uv run main.py

test:
	uv run pytest -v
