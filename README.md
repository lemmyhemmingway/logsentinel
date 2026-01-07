# LogSentinel

**LogSentinel** is a modular log ingestion and analysis system designed to parse raw logs (starting with Nginx) into structured data objects. It is built with Python using SOLID principles for easy extensibility.

## Tech Stack
* **Python 3.12+**
* **uv** (Fast dependency management)
* **pytest** (Unit testing)

## Quick Start

### 1. Installation
Ensure you have `uv` installed.
```bash
git clone
cd LogSentinel
uv sync

uv run main.py

uv run pytest -v
```
