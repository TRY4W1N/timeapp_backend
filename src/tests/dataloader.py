from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorCollection

from src.infrastructure.config import Config
from src.infrastructure.database.mongodb.database import DatabaseMongo
from src.infrastructure.database.mongodb.models import CategoryModel, UserModel

T = TypeVar("T")

uuid_gen = lambda: str(uuid4())
user_uuid_gen = lambda: f"user_{uuid_gen()}"
category_uuid_gen = lambda: f"category_{uuid_gen()}"


class EntityLoader(ABC, Generic[T]):

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self.collection = collection

    @abstractmethod
    async def create(self) -> T: ...

    async def get(self) -> T:
        raise NotImplementedError()

    async def _get(self, fltr: dict) -> dict:
        return await self.collection.find_one(fltr)  # type: ignore


class UserLoader(EntityLoader[UserModel]):

    async def create(
        self,
        uuid: str | None = None,
        name: str | None = None,
        email: str | None = None,
    ) -> UserModel:
        if uuid is None:
            uuid = user_uuid_gen()
        if name is None:
            name = uuid_gen()
        if email is None:
            email = uuid_gen()
        insert_result = await self.collection.insert_one(
            dict(
                uuid=uuid,
                name=name,
                email=email,
            )
        )
        assert insert_result.acknowledged
        created_model = await self.collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        data = dict(**created_model)
        return UserModel(
            uuid=data["uuid"],
            name=data["name"],
            email=data["email"],
        )

    async def get(self, fltr: dict) -> UserModel:
        data = await self._get(fltr=fltr)
        return UserModel(
            uuid=data["uuid"],
            name=data["name"],
            email=data["email"],
        )


class CategoryLoader(EntityLoader[CategoryModel]):

    async def create(
        self,
        uuid: str | None = None,
        user_uuid: str | None = None,
        name: str | None = None,
        icon: str | None = None,
        icon_color: str | None = None,
        position: int = 0,
        disabled: bool = False,
    ) -> CategoryModel:
        if uuid is None:
            uuid = category_uuid_gen()
        if user_uuid is None:
            user_uuid = user_uuid_gen()
        if name is None:
            name = uuid_gen()
        if icon is None:
            icon = uuid_gen()
        if icon_color is None:
            icon_color = uuid_gen()
        insert_result = await self.collection.insert_one(
            dict(
                uuid=uuid,
                user_uuid=user_uuid,
                name=name,
                icon=icon,
                icon_color=icon_color,
                position=position,
                disabled=disabled,
            )
        )
        assert insert_result.acknowledged
        created_model = await self.collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        data = dict(**created_model)
        return CategoryModel(
            uuid=data["uuid"],
            user_uuid=data["user_uuid"],
            name=data["name"],
            disabled=data["disabled"],
            icon=data["icon"],
            icon_color=data["icon_color"],
            position=data["position"],
        )

    async def get(self, fltr: dict) -> CategoryModel:
        data = await self._get(fltr=fltr)
        return CategoryModel(
            uuid=data["uuid"],
            user_uuid=data["user_uuid"],
            name=data["name"],
            disabled=data["disabled"],
            icon=data["icon"],
            icon_color=data["icon_color"],
            position=data["position"],
        )


class Dataloader:

    def __init__(self, database: DatabaseMongo, config: Config) -> None:
        self._database = database
        self._config = config

    @property
    def category_loader(self) -> CategoryLoader:
        collection = self._database.get_collection(name=self._config.MONGODB_COLLECTION_CATEGORY)
        return CategoryLoader(collection=collection)

    @property
    def user_loader(self) -> UserLoader:
        collection = self._database.get_collection(name=self._config.MONGODB_COLLECTION_USER)
        return UserLoader(collection=collection)

    async def __aenter__(self):
        print()
        await self._delete_created_all()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._delete_created_all()
        return

    async def _delete_created_all(self):
        for collection in self._database._get_collection_all():
            await collection.drop()
