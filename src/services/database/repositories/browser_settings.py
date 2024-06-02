from typing import Optional, List

from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClientSession
from pydantic import UUID4

from services.browser.schemas import BrowserSettings


class BrowserSettingsRepository:
    def __init__(
        self,
        database: AsyncIOMotorDatabase,
        session: Optional[AsyncIOMotorClientSession],
    ):
        self.database = database
        self.session = session
        self.collection = self.database.get_collection("browser_settings")

    async def create(self, settings: BrowserSettings) -> None:
        document = settings.model_dump(mode="json")
        await self.collection.insert_one(document=document, session=self.session)
        return None

    async def get_by_name(self, name: UUID4) -> Optional[BrowserSettings]:
        document = await self.collection.find_one(
            filter={"name": str(name)}, session=self.session
        )
        if document is None:
            return None
        return BrowserSettings.model_validate(document)

    async def get_list(self) -> List[BrowserSettings]:
        result: List[BrowserSettings] = []
        async for document in self.collection.find():
            result.append(BrowserSettings.model_validate(document))

        return result

    async def update_by_name(self, name: UUID4, settings: BrowserSettings) -> bool:
        result = await self.collection.replace_one(
            filter={"name": str(name)},
            replacement=settings.model_dump(mode="json"),
            session=self.session,
        )
        return result.matched_count > 0
