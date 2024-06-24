from src.domain.ctx.user.dto import UserCreateDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)


class UserGatewayMongo(GatewayMongoBase, UserGateway):

    def __init__(self, collection: MongoCollectionType) -> None:
        self.collection = collection

    async def is_exist(self, uuid: UserId) -> bool:
        return super().is_exist(uuid)  # type: ignore

    async def get(self, uuid: UserId) -> UserEntity:
        return await super().get(uuid)  # type: ignore

    async def create(self, user: UserCreateDTO) -> UserEntity:
        return super().create(user)  # type: ignore
