from pymongo import ReturnDocument

from src.domain.common.exception.base import EntityNotCreated, EntityNotFound
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import IntervalModel


class IntervalGatewayMongo(GatewayMongoBase, IntervalGateway):

    def __init__(self, interval_collection: MongoCollectionType, category_collection: MongoCollectionType) -> None:
        self.interval_collection = interval_collection
        self.category_collection = category_collection

    async def start(self, user: UserEntity, category_uuid: CategoryId, started_at: int) -> IntervalStartDTO:
        category_filter = {"uuid": category_uuid, "user_uuid": user.uuid}
        category = await self.category_collection.find_one(filter=category_filter)
        if category is None:
            raise EntityNotFound(msg=f"{category_uuid=}")

        interval_filter = {
            "category_uuid": category_uuid,
            "user_uuid": user.uuid,
            "end_at": {"$eq": None},
        }
        interval_data_query = self.interval_collection.aggregate(
            pipeline=[{"$match": interval_filter}], allowDiskUse=True
        )
        interval_data_list = await interval_data_query.to_list(length=None)
        if len(interval_data_list) != 0:
            for interval in interval_data_list:
                fltr = {"uuid": interval["uuid"]}
                await self.interval_collection.find_one_and_update(filter=fltr, update={"$set": {"end_at": started_at}})

        model = IntervalModel(
            uuid=self.gen_uuid(),
            user_uuid=user.uuid,
            category_uuid=category_uuid,
            started_at=started_at,
            end_at=None,
        )
        insert_one = await self.interval_collection.insert_one(model.to_dict())
        created_model = await self.interval_collection.find_one(filter={"_id": insert_one.inserted_id})
        if created_model is None:
            raise EntityNotCreated(msg=f"{user.uuid=}, {category_uuid=}")

        return IntervalStartDTO(
            user_uuid=UserId(user.uuid),
            category_uuid=CategoryId(category_uuid),
            interval_uuid=IntervalId(created_model["uuid"]),
        )

    async def stop(self, user: UserEntity, category_uuid: CategoryId, stopped_at: int) -> IntervalStopDTO:
        category_filter = {"uuid": category_uuid, "user_uuid": user.uuid}
        category = await self.category_collection.find_one(filter=category_filter)
        if category is None:
            raise EntityNotFound(msg=f"{category_uuid=}")

        fltr = {"category_uuid": category_uuid, "user_uuid": user.uuid}
        update_one = await self.interval_collection.find_one_and_update(
            filter=fltr, update={"$set": {"end_at": stopped_at}}, return_document=ReturnDocument.AFTER
        )
        if update_one is None:
            raise EntityNotFound(msg=f"{category_uuid}")
        return IntervalStopDTO(user_uuid=user.uuid, category_uuid=category_uuid, interval_uuid=update_one["uuid"])

    async def clear(self, user: UserEntity, category_uuid: CategoryId) -> IntervalClearDTO:
        interval_filter = {"user_uuid": user.uuid, "category_uuid": category_uuid}
        interval_delete_execution = await self.interval_collection.delete_many(filter=interval_filter)
        assert interval_delete_execution.acknowledged

        return IntervalClearDTO(
            user_uuid=user.uuid, category_uuid=category_uuid, interval_count=interval_delete_execution.deleted_count
        )
