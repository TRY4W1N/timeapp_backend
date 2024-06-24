from dataclasses import dataclass

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class IntervalStartDTO:
    user_uuid: UserId
    category_uuid: CategoryId
    interval_uuid: IntervalId


@dataclass
class IntervalStopDTO:
    user_uuid: UserId
    category_uuid: CategoryId
    interval_uuid: IntervalId


@dataclass
class IntervalClearDTO:
    user_uuid: UserId
    category_uuid: CategoryId
