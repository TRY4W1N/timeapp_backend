from pydantic import BaseModel

from src.domain.common.types.unset import UNSET, UnsetType
from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryDeleteDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.entity import CategoryEntity, CategoryTrackInfo
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId


class CategorySchema(BaseModel):
    uuid: CategoryId
    user_uuid: UserId
    name: str
    active: bool
    icon: str
    icon_color: str
    position: int
    track_info: CategoryTrackInfo

    @classmethod
    def from_obj(cls, category_obj: CategoryEntity) -> "CategorySchema":
        return CategorySchema(
            user_uuid=category_obj.user_uuid,
            uuid=category_obj.uuid,
            name=category_obj.name,
            active=category_obj.active,
            icon=category_obj.icon,
            icon_color=category_obj.icon_color,
            position=category_obj.position,
            track_info=category_obj.track_info,
        )


class CategorySListSchema(BaseModel):
    items: list[CategorySchema]

    @classmethod
    def from_obj(cls, category_list: list[CategoryEntity]) -> "CategorySListSchema":
        items = [
            CategorySchema(
                uuid=obj.uuid,
                user_uuid=obj.user_uuid,
                name=obj.name,
                active=obj.active,
                icon=obj.icon,
                icon_color=obj.icon_color,
                position=obj.position,
                track_info=obj.track_info,
            )
            for obj in category_list
        ]
        return CategorySListSchema(items=items)


class CategoryFilterSchema(BaseModel):
    name__like: str | None = None

    def to_obj(self) -> CategoryFilterDTO:
        return CategoryFilterDTO(**self.model_dump(exclude_unset=True))


class CategoryCreateSchema(BaseModel):
    name: str
    icon: str
    icon_color: str
    position: int

    def to_obj(self) -> CategoryCreateDTO:
        return CategoryCreateDTO(**self.model_dump(exclude_unset=True))


class CategoryUpdateSchema(BaseModel):
    name: str | None = None
    icon: str | None = None
    active: bool | None = None
    icon_color: str | None = None
    position: int | None = None

    def to_obj(self) -> CategoryUpdateDTO:
        return CategoryUpdateDTO(
            **self.model_dump(exclude_unset=True)
        )


class CategoryDeleteSchema(BaseModel):
    category_uuid: CategoryId
    interval_count: int

    @classmethod
    def from_obj(cls, category_obj: CategoryDeleteDTO) -> "CategoryDeleteSchema":
        return CategoryDeleteSchema(
            category_uuid=category_obj.category_uuid, interval_count=category_obj.interval_count
        )
