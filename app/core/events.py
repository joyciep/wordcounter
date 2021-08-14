from fastapi import FastAPI
from app.db.session import initialize_db, engine
from app.core.config import settings


def create_startup_handler():
    """Initialize database in app startup"""

    async def start_app() -> None:
        if settings.create_tables:
            await initialize_db()

    return start_app


def create_shutdown_handler():
    """Close and cleanup connections in app shutdown"""

    async def stop_app() -> None:
        await engine.dispose()

    return stop_app
