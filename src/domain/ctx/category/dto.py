from dataclasses import dataclass

from src.domain.common.dto.unset import UnsetDTO
from src.domain.common.types.unset import UNSET, UnsetType
from src.domain.ctx.category.interface.types import CategoryId


@dataclass
class CategoryCreateDTO:
    name: str
    icon: str
    icon_color: str
    position: int


@dataclass
class CategoryUpdateDTO(UnsetDTO):
    name: str | UnsetType = UNSET
    icon: str | UnsetType = UNSET
    active: bool | UnsetType = UNSET
    icon_color: str | UnsetType = UNSET
    position: int | UnsetType = UNSET


@dataclass
class CategoryFilterDTO(UnsetDTO):
    name__like: str | UnsetType = UNSET


@dataclass
class CategoryDeleteDTO:
    category_uuid: CategoryId
    interval_count: int
