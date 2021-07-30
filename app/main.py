from fastapi import FastAPI

from app.api import wordcount
from app.core.config import settings, VERSION
from app.core.events import create_startup_handler, create_shutdown_handler


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name, debug=settings.debug, version=VERSION
    )
    application.add_event_handler("startup", create_startup_handler())
    application.add_event_handler("shutdown", create_shutdown_handler())
    application.include_router(wordcount.router)
    return application


app = get_application()
