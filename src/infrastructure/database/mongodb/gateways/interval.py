from datetime import datetime
from pytz import timezone

from pymongo import ReturnDocument

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.domain.ctx.interval.entity import IntervalEntity
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.exception import DocumentNotCreated, DocumentNotUpdated
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import IntervalModel

def get_user_datetime_in_timestamp(user_utc: str) -> int:
    user_utc_datetime = datetime.now(timezone(user_utc))
    timestamp = int(round(user_utc_datetime.timestamp()))
    return timestamp


class IntervalGatewayMongo(GatewayMongoBase, IntervalGateway):

    def __init__(self, collection: MongoCollectionType) -> None:
        self.collection = collection

    async def start(self, user: UserEntity, category_uuid: CategoryId) -> IntervalStartDTO:
        started_datetime = get_user_datetime_in_timestamp(user_utc=user.utc)

        model = IntervalModel(
            uuid=self.gen_uuid(), user_uuid=user.uuid, category_uuid=category_uuid, started_at=started_datetime, end_at=None
        )
        insert_one = await self.collection.insert_one(model.to_dict())
        created_model = await self.collection.find_one(filter={"_id": insert_one.inserted_id})
        if created_model is None:
            raise DocumentNotCreated(f"{user.uuid=}, {category_uuid=}")
        return IntervalStartDTO(
            user_uuid=UserId(user.uuid),
            category_uuid=CategoryId(category_uuid),
            interval_uuid=IntervalId(insert_one.inserted_id),
        )

    async def stop(self, user: UserEntity, category_uuid: CategoryId) -> IntervalStopDTO:
        stopped_datetime = get_user_datetime_in_timestamp(user_utc=user.utc)
        fltr = {"category_uuid": category_uuid, "user_uuid": user.uuid}
        update_one = await self.collection.find_one_and_update(filter=fltr, update={"$set": {"end_at": stopped_datetime}}, return_document=ReturnDocument.AFTER)
        
        assert update_one
        return IntervalStopDTO(user_uuid=user.uuid, category_uuid=category_uuid, interval_uuid=update_one["uuid"])

    async def clear(self, user: UserEntity, category_uuid: CategoryId) -> IntervalClearDTO:
        return await super().clear(user_uuid, category_uuid)  # type: ignore
