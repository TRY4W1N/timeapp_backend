from dataclasses import dataclass

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class CategoryTrackCurrent:
    interval_uuid: IntervalId
    category_uuid: CategoryId
    started_at: int


@dataclass
class CategoryEntity:
    uuid: CategoryId
    user_uuid: UserId
    name: str
    active: bool
    icon: str
    color: str
    position: int
    track_current: CategoryTrackCurrent | None
