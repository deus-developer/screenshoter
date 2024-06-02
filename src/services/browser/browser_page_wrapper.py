from typing import Optional, Literal

from playwright.async_api import Page, FloatRect

from services.browser.schemas import ClipSettings


class PageWrapper:
    def __init__(self, page: Page):
        self.page = page

    async def goto(
        self,
        url: str,
        timeout: float = 60.0,
        wait_until: Literal[
            "commit", "domcontentloaded", "load", "networkidle"
        ] = "load",
        referer: Optional[str] = None,
    ):
        await self.page.goto(
            url=url, wait_until=wait_until, timeout=timeout * 1000, referer=referer
        )

    async def take_screenshot(
        self,
        timeout: Optional[int] = None,
        media_type: Literal["jpeg", "png"] = "png",
        quality: Optional[int] = None,
        omit_background: bool = False,
        full_page: bool = False,
        clip_settings: Optional[ClipSettings] = None,
        animations: Literal["allow", "disabled"] = "disabled",
    ) -> bytes:
        clip: Optional[FloatRect] = None

        if clip_settings:
            clip: FloatRect = {
                "x": clip_settings.x,
                "y": clip_settings.y,
                "width": clip_settings.width,
                "height": clip_settings.height,
            }

        if media_type == "png":
            quality = None

        buffer = await self.page.screenshot(
            timeout=timeout,
            type=media_type,
            quality=quality,
            omit_background=omit_background,
            full_page=full_page,
            clip=clip,
            animations=animations,
            path=None,
        )
        return buffer

    async def aclose(self) -> None:
        await self.page.close(run_before_unload=False)
