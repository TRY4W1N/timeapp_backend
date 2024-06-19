from collections.abc import AsyncIterable

import motor.motor_asyncio
from dishka import Provider, Scope, provide
from motor.motor_asyncio import AsyncIOMotorClient

from src.infrastructure.database.mongodb.database import (
    DatabaseMongo,
    DatabaseMongoImplement,
)
from src.infrastructure.di.alias import ConfigType


class DatabaseProvider(Provider):
    component = "DATABASE"

    @provide(scope=Scope.APP)
    async def get_client(self, config: ConfigType) -> AsyncIterable[AsyncIOMotorClient]:
        client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)
        try:
            yield client
        finally:
            client.close()

    @provide(scope=Scope.APP)
    async def get_database(
        self, client: AsyncIOMotorClient, config: ConfigType
    ) -> AsyncIterable[DatabaseMongoImplement]:
        database = client.get_database(name=config.MONGODB_DATABASE)
        allow_collection = [
            config.MONGODB_COLLECTION_USER,
            config.MONGODB_COLLECTION_CATEGORY,
            config.MONGODB_COLLECTION_TIMEDAY,
            config.MONGODB_COLLECTION_TIMEALL,
            config.MONGODB_COLLECTION_INTERVAL,
        ]
        yield DatabaseMongoImplement(database=database, allow_collection=allow_collection)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, client: AsyncIOMotorClient, database: DatabaseMongoImplement
    ) -> AsyncIterable[DatabaseMongo]:
        async with await client.start_session():
            yield database