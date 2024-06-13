from src.domain.ctx.category.dto import CategoryAddDTO
from src.domain.ctx.category.entity import CategoryEntity
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import CategoryModel


class CategoryGatewayMongo(GatewayMongoBase, CategoryGateway):

    def __init__(self, collection: MongoCollectionType) -> None:
        self.collection = collection

    async def add(self, user_uuid: str, obj: CategoryAddDTO) -> CategoryEntity:
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
        return CategoryEntity(
            uuid=created_model_dict["uuid"],
            user_uuid=created_model_dict["user_uuid"],
            name=created_model_dict["name"],
            disabled=created_model_dict["disabled"],
            icon=created_model_dict["icon"],
            icon_color=created_model_dict["icon_color"],
            position=created_model_dict["position"],
            on_track=False,
        )
