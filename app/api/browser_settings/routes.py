from typing import Literal, List

from fastapi import APIRouter
from pydantic import UUID4

from api.depends import BrowserSettingsServiceDeps
from services.browser.schemas import BrowserSettings

router = APIRouter()


@router.post("/settings", summary="Создать контекст")
async def create_settings(
    settings: BrowserSettings,
    browser_settings_service: BrowserSettingsServiceDeps,
) -> Literal[True]:
    return await browser_settings_service.create(settings=settings)


@router.get("/settings/list", summary="Получить все контексты")
async def get_settings_by_name(
    browser_settings_service: BrowserSettingsServiceDeps,
) -> List[BrowserSettings]:
    return await browser_settings_service.get_list()


@router.get("/settings/{name}", summary="Получить контекст")
async def get_settings_by_name(
    name: UUID4,
    browser_settings_service: BrowserSettingsServiceDeps,
) -> BrowserSettings:
    return await browser_settings_service.get_by_name(name=name)


@router.patch("/settings/{name}", summary="Изменить контекст")
async def update_settings_by_name(
    name: UUID4,
    settings: BrowserSettings,
    browser_settings_service: BrowserSettingsServiceDeps,
) -> Literal[True]:
    return await browser_settings_service.update_by_name(name=name, settings=settings)
