from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)


class IntervalGatewayMongo(GatewayMongoBase, IntervalGateway):

    def __init__(self, collection: MongoCollectionType) -> None:
        self.collection = collection

    async def start(self, user_uuid: UserId, category_uuid: CategoryId) -> IntervalStartDTO:
        return await super().start(user_uuid, category_uuid)  # type: ignore

    async def stop(self, user_uuid: UserId, category_uuid: CategoryId) -> IntervalStopDTO:
        return await super().stop(user_uuid, category_uuid)  # type: ignore

    async def clear(self, user_uuid: UserId, category_uuid: CategoryId) -> IntervalClearDTO:
        return await super().clear(user_uuid, category_uuid)  # type: ignore
