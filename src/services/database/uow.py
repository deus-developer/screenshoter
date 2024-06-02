from contextlib import asynccontextmanager
from typing import Optional, Union, AsyncGenerator

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorClientSession,
)
from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import (
    Primary,
    PrimaryPreferred,
    Secondary,
    SecondaryPreferred,
    Nearest,
)

from services.database.repositories import BrowserSettingsRepository


class UnitOfWork:
    def __init__(
        self,
        client: AsyncIOMotorClient,
        database: AsyncIOMotorDatabase,
        session: Optional[AsyncIOMotorClientSession] = None,
    ):
        self._client = client
        self._database = database
        self._session = session

        self.browser_settings = BrowserSettingsRepository(self._database, self._session)

    @asynccontextmanager
    async def transaction(
        self,
        read_concern: Optional[ReadConcern] = None,
        write_concern: Optional[WriteConcern] = None,
        read_preference: Optional[
            Union[Primary, PrimaryPreferred, Secondary, SecondaryPreferred, Nearest]
        ] = None,
        max_commit_time_ms: Optional[int] = None,
    ) -> AsyncGenerator["UnitOfWork", None]:
        if self._session is not None:
            raise RuntimeError("Already in transaction")

        async with await self._client.start_session() as session:
            async with session.start_transaction(
                read_concern=read_concern,
                write_concern=write_concern,
                read_preference=read_preference,
                max_commit_time_ms=max_commit_time_ms,
            ):
                yield UnitOfWork(
                    client=self._client,
                    database=self._database,
                    session=session,
                )

    @property
    def database(self) -> AsyncIOMotorDatabase:
        return self._database
