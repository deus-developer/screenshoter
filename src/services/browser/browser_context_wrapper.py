import json
from typing import Any, Dict

from playwright.async_api import BrowserContext

from services.browser.browser_page_wrapper import PageWrapper


class BrowserContextWrapper:
    def __init__(self, browser_context: BrowserContext):
        self.browser_context = browser_context

    async def init(self) -> None:
        init_options: Dict[str, Any] = {
            "webgl_vendor": "Intel Inc.",
            "webgl_renderer": "Intel Iris OpenGL Engine",
            "navigator_vendor": "Google Inc.",
            "navigator_platform": "Win32",
            "languages": ["ru-RU", "ru", "en-US", "en"],
            "runOnInsecureOrigins": None,
        }
        init_options_json = json.dumps(init_options)
        init_options_script = f"const opts = {init_options_json};"

        await self.browser_context.add_init_script(script=init_options_script)

        await self.browser_context.add_init_script(path="javascript/utils.js")
        await self.browser_context.add_init_script(
            path="javascript/generate.magic.arrays.js"
        )

        await self.browser_context.add_init_script(path="javascript/chrome.app.js")
        await self.browser_context.add_init_script(path="javascript/chrome.csi.js")
        await self.browser_context.add_init_script(path="javascript/chrome.hairline.js")
        await self.browser_context.add_init_script(
            path="javascript/chrome.load.times.js"
        )
        await self.browser_context.add_init_script(path="javascript/chrome.runtime.js")

        await self.browser_context.add_init_script(
            path="javascript/iframe.contentWindow.js"
        )

        await self.browser_context.add_init_script(path="javascript/media.codecs.js")

        await self.browser_context.add_init_script(
            path="javascript/navigator.languages.js"
        )
        await self.browser_context.add_init_script(
            path="javascript/navigator.permissions.js"
        )
        await self.browser_context.add_init_script(
            path="javascript/navigator.platform.js"
        )
        await self.browser_context.add_init_script(
            path="javascript/navigator.plugins.js"
        )
        await self.browser_context.add_init_script(
            path="javascript/navigator.vendor.js"
        )
        await self.browser_context.add_init_script(
            path="javascript/navigator.webdriver.js"
        )

        await self.browser_context.add_init_script(
            path="javascript/window.outerdimensions.js"
        )
        await self.browser_context.add_init_script(path="javascript/webgl.vendor.js")

    async def aclose(self) -> None:
        await self.browser_context.close()

    async def new_page(self) -> PageWrapper:
        page = await self.browser_context.new_page()
        page_wrapped = PageWrapper(page=page)
        return page_wrapped

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
