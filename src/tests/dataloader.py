import random
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Generic, TypeVar
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorCollection

from src.infrastructure.config import ConfigBase
from src.infrastructure.database.mongodb.database import DatabaseMongo
from src.infrastructure.database.mongodb.models import (
    CategoryModel,
    IntervalModel,
    TimeAllModel,
    UserModel,
)

T = TypeVar("T")

uuid_gen = lambda: str(uuid4())
user_uuid_gen = lambda: f"user_{uuid_gen()}"
category_uuid_gen = lambda: f"category_{uuid_gen()}"
interval_uuid_gen = lambda: f"interval_{uuid_gen()}"
time_all_uuid_gen = lambda: f"time_all_{uuid_gen()}"


class EntityLoader(ABC, Generic[T]):

    def __init__(self, collection: AsyncIOMotorCollection, database: DatabaseMongo, config: ConfigBase) -> None:
        self._collection = collection
        self._database = database
        self._config = config

    @abstractmethod
    async def create(self) -> T: ...

    async def get(self) -> T:
        raise NotImplementedError()

    async def _get(self, fltr: dict) -> dict:
        select = await self._collection.find_one(fltr)  # type: ignore
        if select is None:
            raise Exception(f"Not found {self.__class__.__name__} with fltr={fltr}")
        return select


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

        insert_result = await self._collection.insert_one(
            dict(
                uuid=uuid,
                name=name,
                email=email,
            )
        )
        assert insert_result.acknowledged
        created_model = await self._collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        data = dict(**created_model)
        return UserModel(uuid=data["uuid"], name=data["name"], email=data["email"])

    async def get(self, fltr: dict) -> UserModel:
        data = await self._get(fltr=fltr)
        return UserModel(uuid=data["uuid"], name=data["name"], email=data["email"])


class IntervalLoader(EntityLoader[IntervalModel]):

    async def create_many(self, models: list[IntervalModel]) -> list[IntervalModel]:
        insert_result = await self._collection.insert_many([model.to_dict() for model in models])
        assert insert_result.acknowledged
        created_models = await self._collection.find().to_list(length=None)
        return [IntervalModel.from_dict(dict(**model)) for model in created_models]

    async def create(
        self,
        user_uuid: str,
        category_uuid: str,
        uuid: str | None = None,
        started_at: int | None = None,
        end_at: int | None = None,
    ) -> IntervalModel:
        if uuid is None:
            uuid = interval_uuid_gen()
        if started_at is None:
            started_at = int(datetime.now().timestamp())
        insert_result = await self._collection.insert_one(
            IntervalModel(
                uuid=uuid,
                user_uuid=user_uuid,
                category_uuid=category_uuid,
                started_at=started_at,
                end_at=end_at,
            ).to_dict()
        )
        assert insert_result.acknowledged
        created_model = await self._collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        model = IntervalModel.from_dict(dict(**created_model))
        return model

    async def get(self, fltr: dict) -> IntervalModel:
        data = await self._get(fltr=fltr)
        return IntervalModel.from_dict(data)

    async def get_lst(self, fltr: dict) -> list[IntervalModel]:
        data = self._collection.find(fltr)
        models = await data.to_list(length=None)
        return [IntervalModel.from_dict(dict(**model)) for model in models]


class TimeAllLoader(EntityLoader[TimeAllModel]):
    async def create(
        self,
        uuid: str | None = None,
        user_uuid: str | None = None,
        category_uuid: str | None = None,
        time_total: int | None = None,
    ) -> TimeAllModel:
        if uuid is None:
            uuid = time_all_uuid_gen()
        if user_uuid is None:
            user_uuid = user_uuid_gen()
        if category_uuid is None:
            category_uuid = category_uuid_gen()
        if time_total is None:
            time_total = int(datetime.now().timestamp())
        insert_result = await self._collection.insert_one(
            TimeAllModel(uuid=uuid, user_uuid=user_uuid, category_uuid=category_uuid, time_total=time_total).to_dict()
        )
        created_model = await self._collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        model = TimeAllModel.from_dict(dict(**created_model))
        return model

    async def get(self, fltr: dict) -> TimeAllModel:
        data = await self._get(fltr=fltr)
        return TimeAllModel.from_dict(data=data)


class CategoryLoader(EntityLoader[CategoryModel]):

    async def create_many(self, models: list[CategoryModel]) -> list[CategoryModel]:
        insert_result = await self._collection.insert_many([model.to_dict() for model in models])
        assert insert_result.acknowledged
        created_models = await self._collection.find().to_list(length=None)
        return [CategoryModel.from_dict(dict(**model)) for model in created_models]

    async def create(
        self,
        uuid: str | None = None,
        user_uuid: str | None = None,
        name: str | None = None,
        icon: str | None = None,
        icon_color: str | None = None,
        position: int = 0,
        active: bool = True,
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
        insert_result = await self._collection.insert_one(
            CategoryModel(
                uuid=uuid,
                user_uuid=user_uuid,
                name=name,
                icon=icon,
                icon_color=icon_color,
                position=position,
                active=active,
            ).to_dict()
        )
        assert insert_result.acknowledged
        created_model = await self._collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        model = CategoryModel.from_dict(dict(**created_model))
        return model

    async def get(self, fltr: dict) -> CategoryModel:
        data = await self._get(fltr=fltr)
        return CategoryModel.from_dict(data)


class Dataloader:

    def __init__(self, database: DatabaseMongo, config: ConfigBase) -> None:
        self._database = database
        self._config = config

    @property
    def time_all_loader(self) -> TimeAllLoader:
        collection = self._database.get_collection(name=self._config.MONGODB_COLLECTION_TIMEALL)
        return TimeAllLoader(collection=collection, database=self._database, config=self._config)

    @property
    def interval_loader(self) -> IntervalLoader:
        collection = self._database.get_collection(name=self._config.MONGODB_COLLECTION_INTERVAL)
        return IntervalLoader(collection=collection, database=self._database, config=self._config)

    @property
    def category_loader(self) -> CategoryLoader:
        collection = self._database.get_collection(name=self._config.MONGODB_COLLECTION_CATEGORY)
        return CategoryLoader(collection=collection, database=self._database, config=self._config)

    @property
    def user_loader(self) -> UserLoader:
        collection = self._database.get_collection(name=self._config.MONGODB_COLLECTION_USER)
        return UserLoader(collection=collection, database=self._database, config=self._config)

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

    async def generate_category_list(self, user_uuid: str, count: int, interval_count_per_one: int):
        category_models = []
        interval_models = []
        for _ in range(count):
            category_model = CategoryModel(
                uuid=category_uuid_gen(),
                user_uuid=user_uuid,
                name=uuid_gen(),
                icon=uuid_gen(),
                icon_color=uuid_gen(),
            )
            category_models.append(category_model)
            end_interval_exist = False
            for _ in range(interval_count_per_one):
                end_at = int((datetime.now() - timedelta(hours=1)).timestamp())
                if random.randint(0, 1) and end_interval_exist is False:
                    end_at = None
                    end_interval_exist = True
                interval_model = IntervalModel(
                    uuid=uuid_gen(),
                    user_uuid=user_uuid,
                    category_uuid=category_model.uuid,
                    started_at=int((datetime.now() - timedelta(hours=2)).timestamp()),
                    end_at=end_at,
                )
                interval_models.append(interval_model)
        await self.category_loader.create_many(models=category_models)
        await self.interval_loader.create_many(models=interval_models)
