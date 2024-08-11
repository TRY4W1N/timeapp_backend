from abc import ABC, abstractmethod

from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryDeleteDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.entity import CategoryEntity
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId


class CategoryGateway(ABC):

    @abstractmethod
    async def create(self, user_uuid: UserId, obj: CategoryCreateDTO) -> CategoryEntity: ...

    @abstractmethod
    async def update(self, user_uuid: UserId, category_uuid: CategoryId, obj: CategoryUpdateDTO) -> CategoryEntity: ...

    @abstractmethod
    async def delete(self, user_uuid: UserId, category_uuid: CategoryId) -> CategoryDeleteDTO: ...

    @abstractmethod
    async def lst(self, user_uuid: UserId, obj: CategoryFilterDTO) -> list[CategoryEntity]: ...
