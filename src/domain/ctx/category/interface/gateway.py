from abc import ABC, abstractmethod

from src.domain.ctx.category.dto import CategoryAddDTO
from src.domain.ctx.category.entity import CategoryEntity


class CategoryGateway(ABC):

    @abstractmethod
    async def add(self, user_uuid: str, obj: CategoryAddDTO) -> CategoryEntity: ...
