from pydantic import BaseModel

from src.domain.ctx.interval.dto import IntervalStartDTO, IntervalStopDTO


class IntervalStartSchema(BaseModel):
    user_uuid: str
    category_uuid: str
    interval_uuid: str

    @classmethod
    def from_obj(cls, obj: IntervalStartDTO) -> "IntervalStartSchema":
        return IntervalStartSchema(
            user_uuid=obj.user_uuid,
            category_uuid=obj.category_uuid,
            interval_uuid=obj.interval_uuid,
        )


class IntervalStopSchema(BaseModel):
    user_uuid: str
    category_uuid: str
    interval_uuid: str

    @classmethod
    def from_obj(cls, obj: IntervalStopDTO) -> "IntervalStopSchema":
        return IntervalStopSchema(
            user_uuid=obj.user_uuid,
            category_uuid=obj.category_uuid,
            interval_uuid=obj.interval_uuid,
        )
