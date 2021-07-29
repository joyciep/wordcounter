import logging
import sys

from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Word Counter API"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./wordcounter.db"
    create_tables: bool = True


settings = Settings()
VERSION = "1.0.0"
LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.INFO
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
