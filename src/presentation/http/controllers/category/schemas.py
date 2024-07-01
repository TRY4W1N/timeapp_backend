from typing import Union

from pydantic import BaseModel

from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryDeleteDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.entity import CategoryEntity, CategoryTrackCurrent


class CategoryTrackCurrentSchema(BaseModel):
    interval_uuid: str
    category_uuid: str
    started_at: int

    @classmethod
    def from_obj(cls, obj: CategoryTrackCurrent | None) -> Union["CategoryTrackCurrentSchema", None]:
        if obj is None:
            return None
        return CategoryTrackCurrentSchema(
            interval_uuid=obj.interval_uuid,
            category_uuid=obj.category_uuid,
            started_at=obj.started_at,
        )


class CategorySchema(BaseModel):
    uuid: str
    user_uuid: str
    name: str
    active: bool
    icon: str
    icon_color: str
    position: int
    track_current: CategoryTrackCurrentSchema | None

    @classmethod
    def from_obj(cls, obj: CategoryEntity) -> "CategorySchema":
        return CategorySchema(
            user_uuid=obj.user_uuid,
            uuid=obj.uuid,
            name=obj.name,
            active=obj.active,
            icon=obj.icon,
            icon_color=obj.icon_color,
            position=obj.position,
            track_current=CategoryTrackCurrentSchema.from_obj(obj=obj.track_current),
        )


class CategoryListSchema(BaseModel):
    items: list[CategorySchema]

    @classmethod
    def from_obj(cls, obj_list: list[CategoryEntity]) -> "CategoryListSchema":
        items = [CategorySchema.from_obj(obj=obj) for obj in obj_list]
        return CategoryListSchema(items=items)


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
        return CategoryUpdateDTO(**self.model_dump(exclude_unset=True))


class CategoryDeleteSchema(BaseModel):
    user_uuid: str
    category_uuid: str
    interval_count: int

    @classmethod
    def from_obj(cls, obj: CategoryDeleteDTO) -> "CategoryDeleteSchema":
        return CategoryDeleteSchema(
            user_uuid=obj.user_uuid, category_uuid=obj.category_uuid, interval_count=obj.interval_count
        )
