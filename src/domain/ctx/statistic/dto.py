from dataclasses import dataclass

from src.domain.common.dto.fltr import FltrDTO
from src.domain.common.types.unset import UNSET, UnsetType
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class CategoryTimeStatisticDTO:
    category_uuid: CategoryId
    time_total: int
    time_percent: float


@dataclass
class ListCategoryTimeStatisticDTO:
    user_uuid: UserId
    category_list: list[CategoryTimeStatisticDTO]


@dataclass
class StatisticFilterDTO(FltrDTO):
    time_from: int | UnsetType = UNSET
    time_to: int | UnsetType = UNSET
