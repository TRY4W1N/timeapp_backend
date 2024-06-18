from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.entity import CategoryEntity
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import CategoryModel


def build_category_entity_after_create(data: dict) -> CategoryEntity:
    return CategoryEntity(
        uuid=data["uuid"],
        user_uuid=data["user_uuid"],
        name=data["name"],
        disabled=data["disabled"],
        icon=data["icon"],
        icon_color=data["icon_color"],
        position=data["position"],
        on_track=False,
    )


class CategoryGatewayMongo(GatewayMongoBase, CategoryGateway):

    def __init__(self, collection: MongoCollectionType) -> None:
        self.collection = collection

    async def create(self, user_uuid: UserId, obj: CategoryCreateDTO) -> CategoryEntity:
        model = CategoryModel(
            uuid=self.gen_uuid(),
            user_uuid=user_uuid,
            name=obj.name,
            icon=obj.icon,
            icon_color=obj.icon_color,
            position=obj.position,
        )
        insert_result = await self.collection.insert_one(model.to_dict())
        assert insert_result.acknowledged
        created_model = await self.collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        created_model_dict = dict(**created_model)
        return build_category_entity_after_create(created_model_dict)

    async def update(self, user_uuid: UserId, category_uuid: CategoryId, obj: CategoryUpdateDTO) -> CategoryEntity:
        return await super().update(user_uuid, category_uuid, obj)  # type: ignore

    async def delete(self, user_uuid: UserId, category_uuid: CategoryId) -> str:
        return await super().delete(user_uuid, category_uuid)  # type: ignore

    async def lst(self, user_uuid: UserId, obj: CategoryFilterDTO) -> list[CategoryEntity]:
        return await super().lst(user_uuid, obj)  # type: ignore
