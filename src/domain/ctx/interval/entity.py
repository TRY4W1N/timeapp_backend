from dataclasses import dataclass

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class IntervalEntity:
    uuid: IntervalId
    category_uuid: CategoryId
    user_uuid: UserId
    started_at: int
    end_at: int | None
    is_done: bool