from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryDeleteDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.entity import CategoryEntity, CategoryTrackCurrent
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import (
    CategoryModel,
    CategoryTrackCurrentSubModel,
)


def build_category_entity(model: CategoryModel, track_current: CategoryTrackCurrentSubModel | None) -> CategoryEntity:
    track_current_dto = None
    if track_current is not None:
        track_current_dto = CategoryTrackCurrent(
            category_uuid=CategoryId(track_current.category_uuid),
            interval_uuid=IntervalId(track_current.interval_uuid),
            started_at=track_current.started_at,
        )
    return CategoryEntity(
        uuid=CategoryId(model.uuid),
        user_uuid=UserId(model.user_uuid),
        name=model.name,
        active=model.active,
        icon=model.icon,
        icon_color=model.icon_color,
        position=model.position,
        track_current=track_current_dto,
    )


class CategoryGatewayMongo(GatewayMongoBase, CategoryGateway):

    def __init__(
        self,
        category_collection: MongoCollectionType,
        interval_collection: MongoCollectionType,
    ) -> None:
        self.category_collection = category_collection
        self.interval_collection = interval_collection

    async def create(self, user_uuid: UserId, obj: CategoryCreateDTO) -> CategoryEntity:
        model = CategoryModel(
            uuid=self.gen_uuid(),
            user_uuid=user_uuid,
            name=obj.name,
            icon=obj.icon,
            icon_color=obj.icon_color,
            position=obj.position,
        )
        insert_result = await self.category_collection.insert_one(model.to_dict())
        assert insert_result.acknowledged
        created_model = await self.category_collection.find_one(filter={"_id": insert_result.inserted_id})
        if created_model is None:
            raise Exception("Fail")
        created_model = CategoryModel.from_dict(dict(**created_model))
        return build_category_entity(model=created_model, track_current=None)

    async def update(self, user_uuid: UserId, category_uuid: CategoryId, obj: CategoryUpdateDTO) -> CategoryEntity:
        return await super().update(user_uuid, category_uuid, obj)  # type: ignore

    async def delete(self, user_uuid: UserId, category_uuid: CategoryId) -> CategoryDeleteDTO:
        category_fltr = {"uuid": category_uuid}
        category_delete_result = await self.category_collection.delete_one(category_fltr)
        assert category_delete_result.acknowledged
        interval_fltr = {"user_uuid": user_uuid, "category_uuid": category_uuid}
        interval_delete_result = await self.interval_collection.delete_many(interval_fltr)
        assert interval_delete_result.acknowledged
        return CategoryDeleteDTO(category_uuid=category_uuid, interval_count=interval_delete_result.deleted_count)

    async def lst(self, user_uuid: UserId, obj: CategoryFilterDTO) -> list[CategoryEntity]:
        return await super().lst(user_uuid, obj)  # type: ignore
