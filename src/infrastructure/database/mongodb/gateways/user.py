import logging

from src.domain.common.exception.base import EntityNotCreated, EntityNotFound
from src.domain.ctx.user.dto import UserCreateDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.const import get_default_categories
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import CategoryModel, UserModel

logger = logging.getLogger(__name__)


def build_user_entity(model: UserModel) -> UserEntity:
    return UserEntity(uuid=UserId(model.uuid), email=model.email, name=model.name)


class UserGatewayMongo(GatewayMongoBase, UserGateway):

    def __init__(self, user_collection: MongoCollectionType, category_collection: MongoCollectionType) -> None:
        self.user_collection = user_collection
        self.category_collection = category_collection

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
        try:
            await self._create_default_categories_for_user(user=user_entity)
        except Exception as e:
            logger.exception(e)
        return user_entity

    async def _create_default_categories_for_user(self, user: UserEntity) -> None:
        default_categories = get_default_categories()
        user_default_categories = []
        for category in default_categories:
            category["user_uuid"] = user.uuid
            category["uuid"] = self.gen_uuid()
            model = CategoryModel.from_dict(category)
            user_default_categories.append(model)

        insert_data = [model.to_dict() for model in user_default_categories]
        result = await self.category_collection.insert_many(documents=insert_data)
        if len(result.inserted_ids) != len(user_default_categories):
            raise EntityNotCreated(msg=f"Some of default category not created for {user.uuid=}")
