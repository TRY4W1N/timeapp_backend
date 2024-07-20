from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.statistic.dto import (
    CategoryTimeStatisticDTO,
    ListCategoryTimeStatisticDTO,
)
from src.domain.ctx.statistic.interface.gateway import StatisticGateway
from src.domain.ctx.user.entity import UserEntity
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)


class StatisticGatewayMongo(GatewayMongoBase, StatisticGateway):
    def __init__(
        self,
        category_collection: MongoCollectionType,
        interval_collection: MongoCollectionType,
        time_all_collection: MongoCollectionType,
    ) -> None:
        self.category_collection = category_collection
        self.interval_collection = interval_collection
        self.time_all_collection = time_all_collection

    async def get_categories_statistic(self, user: UserEntity) -> ListCategoryTimeStatisticDTO:
        user_category_query = self.category_collection.aggregate(
            [{"$match": {"user_uuid": user.uuid}}, {"$project": {"uuid": 1, "_id": 0}}]
        )
        user_category_data = await user_category_query.to_list(length=None)
        if len(user_category_data) == 0:
            raise EntityNotFound(msg=f"Not found category for {user.uuid=}")
        category_dict = {category["uuid"]: 0 for category in user_category_data}

        interval_data_query = self.interval_collection.aggregate(
            [
                {"$match": {"user_uuid": user.uuid}},
                {
                    "$group": {
                        "_id": {
                            "user_uuid": "$user_uuid",
                            "category_uuid": "$category_uuid",
                        },
                        "total_time": {"$sum": {"$subtract": ["$end_at", "$started_at"]}},
                    },
                },
                {
                    "$project": {
                        "_id": 0,
                        "user_uuid": "$_id.user_uuid",
                        "category_uuid": "$_id.category_uuid",
                        "total_time": 1,
                    }
                },
            ]
        )
        interval_res = await interval_data_query.to_list(length=None)

        time_all_query = self.time_all_collection.aggregate(
            [{"$match": {"user_uuid": user.uuid}}, {"$project": {"_id": 0, "uuid": 0}}]
        )
        time_all_res = await time_all_query.to_list(length=None)

        interval_dict = {item["category_uuid"]: item["total_time"] for item in interval_res}
        time_all_dict = {item["category_uuid"]: item["total_time"] for item in time_all_res}

        category_total_time_dict: dict[str, int] = dict()
        for key in set(category_dict):
            category_total_time_dict[key] = (
                category_dict.get(key, 0) + time_all_dict.get(key, 0) + interval_dict.get(key, 0)
            )

        statistic_total_time = sum(value for value in category_total_time_dict.values())
        res = ListCategoryTimeStatisticDTO(user_uuid=user.uuid, category_list=[])

        for category, total_time in category_total_time_dict.items():
            if statistic_total_time == 0:
                time_percent = len(category_total_time_dict) / 100
            else:
                time_percent = round(((total_time / statistic_total_time) * 100), 2)
            res.category_list.append(
                CategoryTimeStatisticDTO(
                    category_uuid=CategoryId(category), total_time=total_time, time_percent=time_percent
                )
            )

        return res
