# src/api/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    print("API Starting up... Loading resources.")

    yield

    # --- SHUTDOWN ---
    print("API Shutting down... Closing resources.")


app = FastAPI(title="LogSentinel", lifespan=lifespan)

app.include_router(router)
