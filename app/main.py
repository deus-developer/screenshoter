import logging
from contextlib import asynccontextmanager, AsyncExitStack

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from playwright.async_api import async_playwright

from api import setup_routes
from config import Settings
from exception_handlers import setup_exception_handlers
from services.browser.browser_wrapper import BrowserWrapper
from services.browser_settings.service import BrowserSettingsService
from services.database.uow import UnitOfWork

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(_: FastAPI):
    settings = Settings()

    async with AsyncExitStack() as stack:
        mongodb_client = AsyncIOMotorClient(str(settings.mongodb_dsn))
        mongodb_database = mongodb_client[settings.mongodb_database_name]

        uow = UnitOfWork(client=mongodb_client, database=mongodb_database)
        browser_settings_service = BrowserSettingsService(uow=uow)

        playwright = await stack.enter_async_context(async_playwright())
        browser = await stack.enter_async_context(BrowserWrapper(playwright=playwright))

        yield {"browser": browser, "browser_settings_service": browser_settings_service}


def build_application() -> FastAPI:
    application = FastAPI(
        title="Screenshot service",
        version="1.0.0",
        lifespan=lifespan,
        contact={
            "name": "Артем Уколов",
            "url": "https://t.me/DeusDeveloper",
            "email": "deusdeveloper@icloud.com",
        },
    )

    setup_routes(application)
    setup_exception_handlers(application)
    return application


app = build_application()
