import pymongo

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
from src.domain.exception.base import EntityNotCreated, EntityNotFound
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
            raise EntityNotCreated(msg=f"Category not created for user_uuid={user_uuid} with data={obj}")
        created_model = CategoryModel.from_dict(dict(**created_model))
        return build_category_entity(model=created_model, track_current=None)

    async def update(self, user_uuid: UserId, category_uuid: CategoryId, obj: CategoryUpdateDTO) -> CategoryEntity:
        category_fltr = {"user_uuid": user_uuid, "uuid": category_uuid}
        update_values = {"$set": {**obj.to_dict(exclude_unset=True)}}
        update_result = await self.category_collection.find_one_and_update(
            category_fltr, update_values, return_document=pymongo.ReturnDocument.AFTER
        )
        if update_result is None:
            raise EntityNotFound(msg=f"Category not updated for user_uuid={user_uuid} with data={obj}")
        category_updated_model = CategoryModel.from_dict(dict(**update_result))
        interval_fltr = {
            "user_uuid": user_uuid,
            "category_uuid": category_uuid,
            "started_at": {"$ne": None},
            "end_at": {"$eq": None},
        }
        interval_data_query = self.interval_collection.aggregate(
            pipeline=[
                {
                    "$match": interval_fltr,
                },
                {
                    "$sort": {
                        "started_at": pymongo.DESCENDING,
                    },
                },
            ],
            allowDiskUse=True,
        )
        interval_tmp_data = await interval_data_query.to_list(length=1)
        interval_data = None
        if len(interval_tmp_data) == 1:
            interval_data = dict(**interval_tmp_data[0])
        track_current_model = CategoryTrackCurrentSubModel.from_dict(interval_data)
        return build_category_entity(model=category_updated_model, track_current=track_current_model)

    async def delete(self, user_uuid: UserId, category_uuid: CategoryId) -> CategoryDeleteDTO:
        category_fltr = {"uuid": category_uuid}
        category_delete_result = await self.category_collection.delete_one(category_fltr)
        assert category_delete_result.acknowledged
        if category_delete_result.deleted_count == 0:
            raise EntityNotFound(
                msg=f"Category not deleted for user_uuid={user_uuid} and category_uuid={category_uuid}"
            )
        interval_fltr = {"user_uuid": user_uuid, "category_uuid": category_uuid}
        interval_delete_result = await self.interval_collection.delete_many(interval_fltr)
        assert interval_delete_result.acknowledged
        return CategoryDeleteDTO(
            user_uuid=user_uuid, category_uuid=category_uuid, interval_count=interval_delete_result.deleted_count
        )

    async def lst(self, user_uuid: UserId, obj: CategoryFilterDTO) -> list[CategoryEntity]:
        # Filter fields assert
        assert obj._count_fields == 2

        ## Category build filter
        category_filter: dict = {"user_uuid": user_uuid}
        if isinstance(obj.name__like, str):
            category_filter["name"] = {"$regex": obj.name__like, "$options": "i"}
        if isinstance(obj.active__eq, bool):
            category_filter["active"] = obj.active__eq

        # Category select
        category_cursor = self.category_collection.aggregate(
            pipeline=[
                {
                    "$match": category_filter,
                },
                {
                    "$sort": {
                        "position": pymongo.ASCENDING,
                    },
                },
            ],
            allowDiskUse=True,
        )
        category_data_list = await category_cursor.to_list(length=None)

        # Interval select
        category_uuid_list = [item["uuid"] for item in category_data_list]
        interval_fltr = {
            "user_uuid": user_uuid,
            "category_uuid": {"$in": category_uuid_list},
            "started_at": {"$ne": None},
            "end_at": {"$eq": None},
        }
        interval_data_query = self.interval_collection.aggregate(
            pipeline=[
                {
                    "$match": interval_fltr,
                },
                {
                    "$sort": {
                        "started_at": pymongo.DESCENDING,
                    },
                },
                {"$limit": 1},
            ],
            allowDiskUse=True,
        )
        interval_data_list = await interval_data_query.to_list(length=None)

        interval_dict = {}
        for item in interval_data_list:
            interval_dict.setdefault(item["category_uuid"], []).append(item)

        category_entity_list: list[CategoryEntity] = []
        for category_item in category_data_list:
            interval_item_list = interval_dict.get(category_item["uuid"], [])
            interval_item = None
            if len(interval_item_list) == 1:
                interval_item = dict(**interval_item_list[0])
            category_model = CategoryModel.from_dict(dict(**category_item))
            track_current_model = CategoryTrackCurrentSubModel.from_dict(interval_item)
            category_entity = build_category_entity(model=category_model, track_current=track_current_model)
            category_entity_list.append(category_entity)
        return category_entity_list
