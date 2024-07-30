from src.domain.common.exception.base import EntityNotCreated, EntityNotFound
from src.domain.ctx.user.dto import UserCreateDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import UserModel
from src.infrastructure.json_handler import read_default_categories_json


def build_user_entity(model: UserModel) -> UserEntity:
    return UserEntity(uuid=UserId(model.uuid), email=model.email, name=model.name)


class UserGatewayMongo(GatewayMongoBase, UserGateway):

    def __init__(self, user_collection: MongoCollectionType, category_collection: MongoCollectionType) -> None:
        self.user_collection = user_collection
        self.category_collection = category_collection

    async def _create_default_categories_for_user(self, user: UserEntity) -> None:
        default_categories = read_default_categories_json()
        user_default_categories = []
        for category in default_categories:
            category["user_uuid"] = user.uuid
            category["uuid"] = self.gen_uuid()
            user_default_categories.append(category)

        result = await self.category_collection.insert_many(documents=user_default_categories)
        if len(result.inserted_ids) != len(user_default_categories):
            raise EntityNotCreated(msg=f"Some of default category not created for {user.uuid=}")

    async def is_exist(self, uuid: UserId) -> bool:
        check_result = await self.user_collection.find_one({"uuid": uuid}, {"uuid": 1})
        if check_result is None:
            return False
        assert uuid == check_result["uuid"]
        return True

    async def get(self, uuid: UserId) -> UserEntity:
        select_result = await self.user_collection.find_one({"uuid": uuid})
        if select_result is None:
            raise EntityNotFound(msg=f"User ({uuid}): Not found")
        model = UserModel.from_dict(dict(**select_result))
        return build_user_entity(model=model)

    async def create(self, user: UserCreateDTO) -> UserEntity:
        model = UserModel(uuid=user.uuid, email=user.email, name=user.name)
        insert_result = await self.user_collection.insert_one(model.to_dict())
        assert insert_result.acknowledged
        created_model = await self.user_collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise EntityNotCreated(msg=f"User: {user}")
        created_model = UserModel.from_dict(dict(**created_model))
        user_entity = build_user_entity(model=created_model)
        await self._create_default_categories_for_user(user=user_entity)
        return user_entity
