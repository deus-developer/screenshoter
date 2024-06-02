import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from config import Settings
from services.database.uow import UnitOfWork


async def main():
    settings = Settings()

    mongodb_client = AsyncIOMotorClient(str(settings.mongodb_dsn))
    mongodb_database = mongodb_client[settings.mongodb_database_name]

    uow = UnitOfWork(client=mongodb_client, database=mongodb_database)

    try:
        await uow.browser_settings.collection.create_index(
            name="name-index",
            keys=["name"],
            unique=True,
        )
    except (Exception,):
        pass


if __name__ == "__main__":
    asyncio.run(main())
