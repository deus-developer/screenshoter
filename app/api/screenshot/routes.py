import asyncio

from fastapi import APIRouter, status, Query
from fastapi.background import BackgroundTasks
from fastapi.responses import Response
from pydantic import UUID4

from api.depends import BrowserSettingsServiceDeps, BrowserWrapperDeps
from api.screenshot.schemas import ScreenshotRequest

router = APIRouter()


@router.post("/screenshot", summary="Сделать скриншот")
async def screenshot(
    name: UUID4,
    request: ScreenshotRequest,
    browser_settings_service: BrowserSettingsServiceDeps,
    browser: BrowserWrapperDeps,
    background_tasks: BackgroundTasks,
):
    browser_settings = await browser_settings_service.get_by_name(name=name)
    browser_context_wrapped = await browser.get_or_create_context(
        settings=browser_settings
    )

    url = str(request.url)
    referer = str(request.referer) if request.referer else None

    page = await browser_context_wrapped.new_page()
    background_tasks.add_task(page.aclose)

    await page.goto(
        url=url, timeout=request.timeout, wait_until="domcontentloaded", referer=referer
    )

    await asyncio.sleep(request.wait)

    content = await page.take_screenshot(
        timeout=request.timeout * 1000,
        media_type="png",
        quality=None,
        omit_background=request.omit_background,
        full_page=request.full_page,
        clip_settings=request.clip_settings,
        animations=request.animations,
    )

    return Response(
        content=content,
        status_code=status.HTTP_200_OK,
        media_type="image/png",
    )
