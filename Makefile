.PHONY: help run test server lint ci

# Default command
help:
	@echo "LogSentinel Management Commands:"
	@echo "  make run       - Run CLI simulation"
	@echo "  make server    - Start FastAPI server"
	@echo "  make test      - Run all unit tests"
	@echo "  make lint      - Check code style and quality"
	@echo "  make ci        - Run all checks (Used in GitHub Actions)"

run:
	uv run main.py

server:
	uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	uv run pytest -v

lint:
	@echo "Running Ruff linter..."
	uv run ruff check .
	@echo "Checking code format..."
	uv run ruff format --check .

# This command combines everything for CI/CD pipelines
ci: lint test
