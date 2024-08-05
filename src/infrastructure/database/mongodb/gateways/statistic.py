from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.statistic.dto import (
    CategoryTimeStatisticDTO,
    ListCategoryTimeStatisticDTO,
    StatisticFilterTimeDayDTO,
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
        time_day_collection: MongoCollectionType,
    ) -> None:
        self.category_collection = category_collection
        self.interval_collection = interval_collection
        self.time_all_collection = time_all_collection
        self.time_day_collection = time_day_collection

    async def get_categories_statistic(
        self, user: UserEntity, fltr: StatisticFilterTimeDayDTO
    ) -> ListCategoryTimeStatisticDTO:
        user_category_query = self.category_collection.aggregate(
            [{"$match": {"user_uuid": user.uuid}}, {"$project": {"uuid": 1, "_id": 0}}]
        )
        user_category_data = await user_category_query.to_list(length=None)
        if len(user_category_data) == 0:
            raise EntityNotFound(msg=f"Not found category for {user.uuid=}")
        user_category_dict = {category["uuid"]: 0 for category in user_category_data}

        if len(fltr.to_dict()) != 0:
            category_time_total_dict = await self._get_time_day_categories_time_total(fltr=fltr, user=user)
        else:
            category_time_total_dict = await self._get_intervals_and_time_all_categories_time_total(
                user=user, user_category_dict=user_category_dict
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

    async def _get_time_day_categories_time_total(
        self, fltr: StatisticFilterTimeDayDTO, user: UserEntity
    ) -> dict[str, int]:
        time_day_match = {"time_day": {}, "user_uuid": user.uuid}
        raw_interval_match = {"user_uuid": user.uuid, "started_at": {}, "end_at": {}}
        if isinstance(fltr.time_from, int):
            time_day_match["time_day"]["$gte"] = fltr.time_from
            raw_interval_match["started_at"]["$gte"] = fltr.time_from
        if isinstance(fltr.time_to, int):
            time_day_match["time_day"]["$lte"] = fltr.time_to
            raw_interval_match["end_at"]["$lte"] = fltr.time_to
        interval_match = {key: value for key, value in raw_interval_match.items() if value != {}}
        interval_data_query = self.interval_collection.aggregate(
            [
                {"$match": interval_match},
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
                        "category_uuid": "$_id.category_uuid",
                        "time_total": 1,
                    }
                },
            ]
        )

        interval_data = await interval_data_query.to_list(length=None)
        time_day_data_query = self.time_day_collection.aggregate(
            [
                {"$match": time_day_match},
                {
                    "$project": {
                        "_id": 0,
                        "category_uuid": "$category_uuid",
                        "time_total": 1,
                    }
                },
            ]
        )
        time_day_res = await time_day_data_query.to_list(length=None)

        if len(time_day_res) == 0 and len(interval_data) == 0:
            raise EntityNotFound(msg=f"There is no records in filter range for {user.uuid}")
        interval_dict = {interval["category_uuid"]: interval["time_total"] for interval in interval_data}
        time_day_dict = {item["category_uuid"]: item["time_total"] for item in time_day_res}
        categories_uuid_set = set(interval_dict.keys()) | set(time_day_dict.keys())

        category_time_total_dict: dict[str, int] = {}
        for key in categories_uuid_set:
            category_time_total_dict[key] = interval_dict.get(key, 0) + time_day_dict.get(key, 0)
        return category_time_total_dict

    async def _get_intervals_and_time_all_categories_time_total(
        self, user: UserEntity, user_category_dict: dict[str, int]
    ) -> dict[str, int]:
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
        for key in user_category_dict:
            category_time_total_dict[key] = (
                user_category_dict[key] + time_all_dict.get(key, 0) + interval_dict.get(key, 0)
            )
        return category_time_total_dict
