from collections.abc import Generator
from datetime import date, datetime, timedelta

import pymongo
from pymongo import DeleteMany, UpdateOne

from src.domain.common.exception.base import EntityNotCreated, EntityNotFound
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import IntervalStartDTO, IntervalStopDTO
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.database.mongodb.gateways.base import (
    GatewayMongoBase,
    MongoCollectionType,
)
from src.infrastructure.database.mongodb.models import IntervalModel


class IntervalGatewayMongo(GatewayMongoBase, IntervalGateway):

    def __init__(self, interval_collection: MongoCollectionType, category_collection: MongoCollectionType) -> None:
        self.interval_collection = interval_collection
        self.category_collection = category_collection

    async def start(self, user: UserEntity, category_uuid: CategoryId) -> IntervalStartDTO:
        started_at = self.get_current_timestamp()

        category_filter = {"uuid": category_uuid, "user_uuid": user.uuid}
        category = await self.category_collection.find_one(filter=category_filter)
        if category is None:
            raise EntityNotFound(msg=f"{category_uuid=}")

        interval_data_list = await self._get_closed_interval_list(user_uuid=user.uuid, category_uuid=category_uuid)

        if len(interval_data_list) != 0:
            await self._correct_opened_interval_list(interval_data_list, started_at)

        model = IntervalModel(
            uuid=self.gen_uuid(),
            user_uuid=user.uuid,
            category_uuid=category_uuid,
            started_at=started_at,
            end_at=None,
        )
        insert_one = await self.interval_collection.insert_one(model.to_dict())
        created_model = await self.interval_collection.find_one(filter={"_id": insert_one.inserted_id})
        if created_model is None:
            raise EntityNotCreated(msg=f"{user.uuid=}, {category_uuid=}")

        return IntervalStartDTO(
            user_uuid=UserId(user.uuid),
            category_uuid=CategoryId(category_uuid),
            interval_uuid=IntervalId(created_model["uuid"]),
        )

    async def stop(self, user: UserEntity, category_uuid: CategoryId) -> IntervalStopDTO:
        stopped_at = self.get_current_timestamp()

        category_filter = {"uuid": category_uuid, "user_uuid": user.uuid}
        category = await self.category_collection.find_one(filter=category_filter)
        if category is None:
            raise EntityNotFound(msg=f"Category not found for user_uuid={user.uuid} with uuid={category_uuid}")

        interval_data_list = await self._get_closed_interval_list(user_uuid=user.uuid, category_uuid=category_uuid)
        if len(interval_data_list) == 0:
            raise EntityNotFound(msg=f"Open intervals not found for user_uuid={user.uuid} with uuid={category_uuid}")

        correct_data = await self._correct_opened_interval_list(interval_data_list, stopped_at)

        last_closed_interval = correct_data[-1]
        return IntervalStopDTO(
            user_uuid=last_closed_interval["user_uuid"],
            category_uuid=last_closed_interval["category_uuid"],
            interval_uuid=last_closed_interval["uuid"],
        )

    async def _get_closed_interval_list(self, user_uuid: UserId, category_uuid: CategoryId) -> list[dict]:
        interval_filter = {
            "category_uuid": category_uuid,
            "user_uuid": user_uuid,
            "end_at": {"$eq": None},
        }
        interval_data_query = self.interval_collection.aggregate(
            pipeline=[
                {"$match": interval_filter},
                {
                    "$sort": {
                        "started_at": pymongo.ASCENDING,
                    },
                },
            ],
            allowDiskUse=True,
        )
        interval_data_list = await interval_data_query.to_list(length=None)
        return interval_data_list

    async def _correct_opened_interval_list(self, interval_data_list: list[dict], end_time: int) -> list[dict]:
        data_list = balancing_interval_list(interval_data_list, end_time)
        data_list = extend_interval_list_per_day(data_list)
        interval_delete_uuid_list = list(
            {item["uuid"] for item in interval_data_list} - {item["uuid"] for item in data_list}
        )
        bulk_operation_list = []
        for item in data_list:
            model = IntervalModel.from_dict(item)
            if model.uuid is None:
                model.uuid = self.gen_uuid()
            bulk_operation_list.append(
                UpdateOne(
                    {"uuid": item["uuid"]},
                    {"$set": model.to_dict()},
                    upsert=True,
                )
            )
        if len(interval_delete_uuid_list) > 0:
            bulk_operation_list.append(
                DeleteMany(
                    {"uuid": {"$in": interval_delete_uuid_list}},
                ),
            )
        await self.interval_collection.bulk_write(bulk_operation_list)
        return data_list


def get_date_range(start_in: datetime, end_in: datetime) -> Generator[date, None, None]:
    start = start_in.date() + timedelta(1)
    end = end_in.date()
    while start <= end:
        yield start
        start += timedelta(1)


def balancing_interval_list(interval_list: list, interval_last_end_at: int) -> list:
    # Remove duplicates by started_at
    interval_list = list({i["started_at"]: i for i in interval_list}.values())

    # One element
    if len(interval_list) == 1:
        interval_list[0]["end_at"] = interval_last_end_at
        return interval_list

    # Balancing
    for i in range(len(interval_list) - 1):
        current_item = interval_list[i]
        next_item = interval_list[i + 1]
        current_item["end_at"] = next_item["started_at"]
        if i + 1 == len(interval_list) - 1:
            next_item["end_at"] = interval_last_end_at
    return interval_list


def split_interval_per_day(start_ts: int, end_ts: int) -> list:
    start = datetime.fromtimestamp(start_ts)
    end = datetime.fromtimestamp(end_ts)
    dates = [datetime.strptime(str(date_iter), "%Y-%m-%d") for date_iter in get_date_range(start, end)] + [start, end]
    dates = sorted(dates)

    diapason = []
    for i in range(len(dates) - 1):
        diapason.append((dates[i], dates[i + 1]))
    return diapason


def extend_interval_list_per_day(interval_list: list) -> list:
    interval_list_new = []
    for interval in interval_list:
        nested_date_intervals = split_interval_per_day(interval["started_at"], interval["end_at"])
        for idx, date_interval in enumerate(nested_date_intervals):
            st, en = date_interval
            interval_list_new.append(
                {
                    "uuid": interval["uuid"] if idx == 0 else None,
                    "user_uuid": interval["user_uuid"],
                    "category_uuid": interval["category_uuid"],
                    "started_at": int(st.timestamp()),
                    "end_at": int(en.timestamp()),
                }
            )

    return interval_list_new
