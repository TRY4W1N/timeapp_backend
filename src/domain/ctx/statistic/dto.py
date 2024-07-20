from dataclasses import dataclass

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class CategoryTimeStatisticDTO:
    category_uuid: CategoryId
    total_time: int
    time_percent: float


@dataclass
class ListCategoryTimeStatisticDTO:
    user_uuid: UserId
    category_list: list[CategoryTimeStatisticDTO]
