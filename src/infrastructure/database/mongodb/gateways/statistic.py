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
                        "time_total": {"$sum": {"$subtract": ["$end_at", "$started_at"]}},
                    },
                },
                {
                    "$project": {
                        "_id": 0,
                        "user_uuid": "$_id.user_uuid",
                        "category_uuid": "$_id.category_uuid",
                        "time_total": 1,
                    }
                },
            ]
        )
        interval_res = await interval_data_query.to_list(length=None)

        time_all_query = self.time_all_collection.aggregate(
            [{"$match": {"user_uuid": user.uuid}}, {"$project": {"_id": 0, "uuid": 0}}]
        )
        time_all_res = await time_all_query.to_list(length=None)

        interval_dict = {item["category_uuid"]: item["time_total"] for item in interval_res}
        time_all_dict = {item["category_uuid"]: item["time_total"] for item in time_all_res}

        category_time_total_dict: dict[str, int] = dict()
        for key in category_dict:
            category_time_total_dict[key] = (
                category_dict[key] + time_all_dict.get(key, 0) + interval_dict.get(key, 0)
            )

        statistic_time_total = sum(value for value in category_time_total_dict.values())
        res = ListCategoryTimeStatisticDTO(user_uuid=user.uuid, category_list=[])

        for category, time_total in category_time_total_dict.items():
            time_percent = round(time_total / statistic_time_total * 100, 2) if statistic_time_total != 0 else 0.0
            res.category_list.append(
                CategoryTimeStatisticDTO(
                    category_uuid=CategoryId(category), time_total=time_total, time_percent=time_percent
                )
            )

        return res
