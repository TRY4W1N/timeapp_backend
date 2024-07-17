from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.time_all.dto import CategoryTimeStatistic, ListCategoryTimeStatistic
from src.domain.ctx.time_all.interface.gateway import TimeAllGateway
from src.domain.ctx.user.entity import UserEntity
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)


class TimeAllGatewayMongo(GatewayMongoBase, TimeAllGateway):
    def __init__(
        self,
        category_collection: MongoCollectionType,
        interval_collection: MongoCollectionType,
        time_all_collection: MongoCollectionType,
    ) -> None:
        self.category_collection = category_collection
        self.interval_collection = interval_collection
        self.time_all_collection = time_all_collection

    async def get_categories_statistic(self, user: UserEntity) -> ListCategoryTimeStatistic:
        category_fltr = {"user_uuid": user.uuid, "active": True}
        user_category_data_query = self.category_collection.aggregate(
            pipeline=[{"$match": category_fltr}, {"$project": {"uuid": 1, "_id": 0}}], allowDiskUse=True
        )
        user_category_list = await user_category_data_query.to_list(length=None)
        if len(user_category_list) == 0:
            raise EntityNotFound(msg=f"Not found categories for {user.uuid=}")
        list_category_total_time = []
        for category in user_category_list:
            interval_fltr = {"user_uuid": user.uuid, "category_uuid": category["uuid"], "end_at": {"$ne": None}}
            interval_data_query = self.interval_collection.aggregate([{"$match": interval_fltr}])
            interval_list = await interval_data_query.to_list(length=None)

            category_total_time = 0
            for interval in interval_list:
                category_total_time += interval["end_at"] - interval["started_at"]

            time_all_flrt = {"user_uuid": user.uuid, "category_uuid": category["uuid"]}
            time_all_category = await self.time_all_collection.find_one(filter=time_all_flrt)
            if time_all_category:
                category_total_time += time_all_category["total_time"]

            res = {"category_uuid": category["uuid"], "total_time": category_total_time}

            list_category_total_time.append(res)

        total_time_of_categories = sum((category["total_time"] for category in list_category_total_time), 0)

        res = ListCategoryTimeStatistic(user_uuid=user.uuid, category_list=[])
        for category in list_category_total_time:
            if total_time_of_categories == 0:
                time_percent = len(list_category_total_time) / 100
            else:
                time_percent = round(((category["total_time"] / total_time_of_categories) * 100), 3)
            res.category_list.append(
                CategoryTimeStatistic(
                    category_uuid=category["category_uuid"],
                    total_time=category["total_time"],
                    time_percent=time_percent,
                )
            )

        return res
