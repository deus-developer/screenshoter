import asyncio
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Optional, Dict

from playwright.async_api import ViewportSize, Geolocation, Playwright
from pydantic import UUID4

from services.browser.browser_context_wrapper import BrowserContextWrapper
from services.browser.schemas import BrowserSettings, ViewportSettings

default_viewport = ViewportSettings(width=1280, height=720)
base_context_folder = Path("/var/lib/screenshoter/")


class BrowserWrapper:
    def __init__(self, playwright: Playwright):
        self.playwright = playwright
        self.stack = AsyncExitStack()

        self.context_by_name: Dict[UUID4, BrowserContextWrapper] = {}
        self.context_lock = asyncio.Lock()

    async def get_or_create_context(
        self, settings: BrowserSettings
    ) -> BrowserContextWrapper:
        async with self.context_lock:
            browser_context_wrapped = self.context_by_name.get(settings.name)
            if browser_context_wrapped:
                return browser_context_wrapped

            browser_context_wrapped = await self.new_context(settings)
            self.context_by_name[settings.name] = browser_context_wrapped
            return browser_context_wrapped

    async def new_context(self, settings: BrowserSettings) -> BrowserContextWrapper:
        viewport_settings = settings.viewport or default_viewport

        viewport: ViewportSize = {
            "width": viewport_settings.width,
            "height": viewport_settings.height,
        }

        geolocation: Optional[Geolocation] = None

        if settings.geolocation:
            geolocation: Geolocation = {
                "latitude": settings.geolocation.latitude,
                "longitude": settings.geolocation.longitude,
                "accuracy": settings.geolocation.accuracy,
            }

        context_folder = base_context_folder / settings.name.hex
        user_data_folder = context_folder / "user_data"
        downloads_folder = context_folder / "downloads"

        browser_context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=user_data_folder,
            channel=None,
            executable_path=None,
            args=None,
            ignore_default_args=None,
            handle_sigint=True,
            handle_sigterm=True,
            handle_sighup=True,
            timeout=30 * 1000,
            env=None,
            headless=False,
            devtools=False,
            proxy=None,
            downloads_path=downloads_folder,
            slow_mo=None,
            viewport=viewport,
            screen=viewport,
            no_viewport=False,
            ignore_https_errors=settings.ignore_https_errors,
            java_script_enabled=settings.java_script_enabled,
            bypass_csp=settings.bypass_csp,
            user_agent=settings.user_agent,
            locale=settings.locale,
            timezone_id=settings.timezone,
            geolocation=geolocation,
            permissions=settings.permissions,
            extra_http_headers=None,
            offline=False,
            http_credentials=None,
            device_scale_factor=settings.device_scale_factor,
            is_mobile=settings.is_mobile,
            has_touch=settings.has_touch,
            color_scheme=settings.color_scheme,
            reduced_motion=None,
            forced_colors=None,
            accept_downloads=settings.accept_downloads,
            traces_dir=None,
            chromium_sandbox=None,
            firefox_user_prefs=None,
            record_har_path=None,
            record_har_omit_content=None,
            record_video_dir=None,
            record_video_size=None,
            base_url=None,
            strict_selectors=None,
            service_workers=settings.service_workers,
            record_har_url_filter=None,
            record_har_mode=None,
            record_har_content=None,
        )

        browser_context_wrapped = BrowserContextWrapper(browser_context=browser_context)
        await self.stack.enter_async_context(browser_context_wrapped)

        return browser_context_wrapped

    async def aclose(self) -> None:
        await self.stack.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
