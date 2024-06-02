from typing import Annotated

from fastapi import Request, Depends

from services.browser.browser_wrapper import BrowserWrapper
from services.browser_settings.service import BrowserSettingsService


def get_browser_wrapper(request: Request) -> BrowserWrapper:
    return request.state.browser


def get_browser_settings_service(request: Request) -> BrowserSettingsService:
    return request.state.browser_settings_service


BrowserWrapperDeps = Annotated[BrowserWrapper, Depends(get_browser_wrapper)]
BrowserSettingsServiceDeps = Annotated[
    BrowserSettingsService, Depends(get_browser_settings_service)
]
