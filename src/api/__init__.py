from fastapi import FastAPI

from .browser_settings.routes import router as browser_settings_router
from .screenshot.routes import router as screenshot_router


def setup_routes(app: FastAPI) -> None:
    app.include_router(browser_settings_router)
    app.include_router(screenshot_router)
