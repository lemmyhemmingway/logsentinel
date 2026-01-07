.PHONY: help run test server

help:
	@echo "Available commands:"
	@echo "  make run    - Run the CLI simulation (Phase 1)"
	@echo "  make server - Run the FastAPI Backend (Phase 2)"
	@echo "  make test   - Run unit tests"

run:
	uv run main.py

test:
	uv run pytest -v

server:
	uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
