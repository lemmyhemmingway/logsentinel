# LogSentinel

**LogSentinel** is a modular log ingestion and analysis system designed to parse raw logs (starting with Nginx) into structured data objects. It is built with Python using SOLID principles for easy extensibility.

## Features
- **Modular Parsers**: Easy to add support for new log formats (Nginx, Apache, Syslog, etc.).
- **Log Agents**: Built-in agents to monitor log sources (like files) and push data to the API.
- **REST API**: FastAPI-powered endpoints for single and batch log processing.

## Tech Stack
* **Python 3.12+**
* **FastAPI** (High-performance API framework)
* **httpx** (Modern HTTP client for agents)
* **uv** (Fast dependency management)
* **pytest** (Unit and integration testing)

## Quick Start

### 1. Installation
Ensure you have `uv` installed.
```bash
git clone https://github.com/lemmyhemmingway/logsentinel.git
cd LogSentinel
uv sync
```

### 2. Available Commands (using Makefile)
The project includes a `Makefile` for common development tasks:

*   **`make server`**: Start the FastAPI server (default: `http://localhost:8000`)
*   **`make test`**: Run all unit and integration tests
*   **`make run`**: Run the CLI log processing simulation
*   **`make lint`**: Run code style and quality checks (Ruff)
*   **`make help`**: Show all available commands

### 3. Using Agents
Agents can be configured in `config.yaml` and instantiated via `AgentFactory`.

Example usage (File Tailing):
```python
from src.agents import AgentFactory, LogSentinelClient
from src.config import ConfigLoader

# 1. Load configuration
config = ConfigLoader.load_config()

# 2. Setup internal client
client = LogSentinelClient(base_url="http://localhost:8000")

# 3. Start agents defined in config
for agent_cfg in config.get("agents", []):
    agent = AgentFactory.create_agent(
        agent_cfg["type"],
        agent_cfg,
        on_line_received=lambda line: client.send_log(agent_cfg["parser_type"], line)
    )
    agent.start()
```

## Testing
To run all tests, simply use:
```bash
make test
```
