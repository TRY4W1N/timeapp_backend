from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.entity import CategoryEntity, CategoryTrackInfo
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import CategoryModel, CategoryTrackInfoSubModel


def build_category_entity(model: CategoryModel, track_info: CategoryTrackInfoSubModel) -> CategoryEntity:
    track_info__interval_uuid = None
    if track_info.interval_uuid is not None:
        track_info__interval_uuid = IntervalId(track_info.interval_uuid)
    return CategoryEntity(
        uuid=CategoryId(model.uuid),
        user_uuid=UserId(model.user_uuid),
        name=model.name,
        active=model.active,
        icon=model.icon,
        icon_color=model.icon_color,
        position=model.position,
        track_info=CategoryTrackInfo(
            category_uuid=CategoryId(track_info.category_uuid),
            active=track_info.active,
            started_at=track_info.started_at,
            interval_uuid=track_info__interval_uuid,
        ),
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
        return build_category_entity(
            model=created_model,
            track_info=CategoryTrackInfoSubModel(
                category_uuid=created_model.uuid, active=False, started_at=None, interval_uuid=None
            ),
        )

    async def update(self, user_uuid: UserId, category_uuid: CategoryId, obj: CategoryUpdateDTO) -> CategoryEntity:
        return await super().update(user_uuid, category_uuid, obj)  # type: ignore

    async def delete(self, user_uuid: UserId, category_uuid: CategoryId) -> str:
        return await super().delete(user_uuid, category_uuid)  # type: ignore

    async def lst(self, user_uuid: UserId, obj: CategoryFilterDTO) -> list[CategoryEntity]:
        return await super().lst(user_uuid, obj)  # type: ignore
