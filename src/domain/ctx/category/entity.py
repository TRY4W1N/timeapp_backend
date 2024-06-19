from dataclasses import dataclass

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.interface.types import UserId

@dataclass
class CategoryTrackInfo:
    category_uuid: CategoryId
    active: bool
    started_at: int | None
    interval_uuid: IntervalId | None

@dataclass
class CategoryEntity:
    uuid: CategoryId
    user_uuid: UserId
    name: str
    active: bool
    icon: str
    icon_color: str
    position: int
    track_info: CategoryTrackInfo
