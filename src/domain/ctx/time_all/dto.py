from dataclasses import dataclass

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class CategoryTimeStatistic:
    category_uuid: CategoryId
    total_time: int
    time_percent: float


@dataclass
class ListCategoryTimeStatistic:
    user_uuid: UserId
    category_list: list[CategoryTimeStatistic]
