from dataclasses import dataclass

from src.domain.common.dto.fltr import FltrDTO
from src.domain.common.dto.unset import UnsetDTO
from src.domain.common.types.unset import UNSET, UnsetType
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId


@dataclass
class CategoryCreateDTO:
    name: str
    icon: str
    color: str
    position: int


@dataclass
class CategoryUpdateDTO(UnsetDTO):
    name: str | UnsetType = UNSET
    icon: str | UnsetType = UNSET
    active: bool | UnsetType = UNSET
    color: str | UnsetType = UNSET
    position: int | UnsetType = UNSET


@dataclass
class CategoryFilterDTO(FltrDTO):
    name__like: str | UnsetType = UNSET
    active__eq: bool | UnsetType = UNSET


@dataclass
class CategoryDeleteDTO:
    user_uuid: UserId
    category_uuid: CategoryId
    interval_count: int
