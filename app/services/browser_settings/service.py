from typing import Literal, List

from pydantic import UUID4
from pymongo.errors import DuplicateKeyError

from services.browser.schemas import BrowserSettings
from services.browser_settings.errors import (
    BrowserSettingsAlreadyExistsError,
    BrowserSettingsNotFoundError,
)
from services.database.uow import UnitOfWork


class BrowserSettingsService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create(self, settings: BrowserSettings) -> Literal[True]:
        try:
            await self.uow.browser_settings.create(settings=settings)
        except DuplicateKeyError:
            raise BrowserSettingsAlreadyExistsError(name=settings.name)

        return True

    async def get_by_name(self, name: UUID4) -> BrowserSettings:
        document = await self.uow.browser_settings.get_by_name(name=name)
        if document is None:
            raise BrowserSettingsNotFoundError(name=name)
        return document

    async def get_list(self) -> List[BrowserSettings]:
        return await self.uow.browser_settings.get_list()

    async def update_by_name(
        self, name: str, settings: BrowserSettings
    ) -> Literal[True]:
        result = await self.uow.browser_settings.update_by_name(
            name=name, settings=settings
        )
        if result:
            return True

        raise BrowserSettingsNotFoundError(name=name)
