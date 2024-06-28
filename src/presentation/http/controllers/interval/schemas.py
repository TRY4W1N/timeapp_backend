from pydantic import BaseModel

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.interface.types import UserId


class IntervalStartSchema(BaseModel):
    user_uuid: UserId
    category_uuid: CategoryId
    interval_uuid: IntervalId

    @classmethod
    def from_obj(cls, interval_obj: IntervalStartDTO) -> "IntervalStartSchema":
        return IntervalStartSchema(
            user_uuid=interval_obj.user_uuid,
            category_uuid=interval_obj.category_uuid,
            interval_uuid=interval_obj.interval_uuid,
        )


class IntervalStopSchema(BaseModel):
    user_uuid: UserId
    category_uuid: CategoryId
    interval_uuid: IntervalId

    @classmethod
    def from_obj(cls, interval_obj: IntervalStopDTO) -> "IntervalStopSchema":
        return IntervalStopSchema(
            user_uuid=interval_obj.user_uuid,
            category_uuid=interval_obj.category_uuid,
            interval_uuid=interval_obj.interval_uuid,
        )


class IntervalClearSchema(BaseModel):
    user_uuid: UserId
    category_uuid: CategoryId

    @classmethod
    def from_obj(cls, interval_obj: IntervalClearDTO) -> "IntervalClearSchema":
        return IntervalClearSchema(user_uuid=interval_obj.user_uuid, category_uuid=interval_obj.category_uuid)
