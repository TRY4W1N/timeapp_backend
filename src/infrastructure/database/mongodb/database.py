from typing import Protocol

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from src.domain.exception.base import CollectionNotFound


class DatabaseMongo(Protocol):

    @property
    def allow_collection(self) -> list[str]: ...

    def get_collection(self, name: str) -> AsyncIOMotorCollection: ...

    def get_collections(self, *names: str) -> tuple[AsyncIOMotorCollection, ...]: ...

    def _get_collection_all(self) -> tuple[AsyncIOMotorCollection, ...]: ...


class DatabaseMongoImplement:

    def __init__(self, database: AsyncIOMotorDatabase, allow_collection: list[str]) -> None:
        self._database = database
        self._allow_collection = allow_collection

    @property
    def allow_collection(self) -> list[str]:
        return self._allow_collection

    def get_collection(self, name: str) -> AsyncIOMotorCollection:
        if name not in self._allow_collection:
            raise CollectionNotFound(f"`{name}` not in allow collection: {self.allow_collection}")
        return self._database[name]

    def get_collections(self, *names: str) -> tuple[AsyncIOMotorCollection, ...]:
        return tuple(self.get_collection(name) for name in names)

    def _get_collection_all(self) -> tuple[AsyncIOMotorCollection, ...]:
        return tuple([self._database[name] for name in self._allow_collection])
