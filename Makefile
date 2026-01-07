.PHONY: help run test server lint check-all

# Default command
help:
	@echo "LogSentinel Management Commands:"
	@echo "  make run       - Run CLI simulation"
	@echo "  make server    - Start FastAPI server"
	@echo "  make test      - Run all unit tests"
	@echo "  make lint      - Check code style and quality"
	@echo "  make check-all - Run linter and tests (Pre-push check)"

# Phase 1: Run CLI logic
run:
	uv run main.py

# Phase 2: Start API server with auto-reload
server:
	uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Run pytest suite
test:
	uv run pytest -v

# Run Ruff for linting and formatting checks
lint:
	@echo "Running Ruff linter..."
	uv run ruff check .
	@echo "Checking code format..."
	uv run ruff format --check .

# Comprehensive check before pushing code
check-all: lint test
	@echo "All checks passed! Ready to push."
