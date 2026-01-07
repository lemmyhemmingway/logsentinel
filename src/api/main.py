from fastapi import FastAPI
from src.config import ConfigLoader
from src.api.routes import router

# 1. Load Configuration
try:
    config = ConfigLoader.load_config()
    app_name = config.get("app", {}).get("name", "LogSentinel")
except Exception:
    app_name = "LogSentinel"

# 2. Initialize App
app = FastAPI(
    title=app_name,
    description="A modular log ingestion and analysis API.",
    version="0.1.0"
)

# 3. Include Routes
# This automatically registers /parse/{parser_type} endpoints
app.include_router(router)
