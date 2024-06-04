from collections.abc import AsyncIterable
import typing
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dishka import Provider, provide, Scope

from src.infrastructure.database.mongodb.database import DatabaseMongoImplement, DatabaseMongo
from src.infrastructure.di.config import config


class DatabaseProvider(Provider):

    @provide(scope=Scope.APP, cache=True)
    async def get_client(self) -> AsyncIterable[AsyncIOMotorClient]:
        print("Mongo client build!")
        client = motor.motor_asyncio.AsyncIOMotorClient(config.MONGODB_URL)
        try:
            yield client
        finally:
            client.close()

    @provide(scope=Scope.APP, cache=True)
    async def get_database(self, client: AsyncIOMotorClient) -> AsyncIterable[DatabaseMongoImplement]:
        print("Mongo database build!")
        database = client.get_database(name=config.MONGODB_DATABASE)
        allow_collection = typing.cast(list[str], config.MONGODB_COLLECTION_LIST)
        yield DatabaseMongoImplement(database=database, allow_collection=allow_collection)
    
    @provide(scope=Scope.REQUEST, cache=False)
    async def get_session(self, client: AsyncIOMotorClient, database: DatabaseMongoImplement) -> AsyncIterable[DatabaseMongo]:
        async with await client.start_session():
            print("Start session")
            yield database
        print("Session is close")