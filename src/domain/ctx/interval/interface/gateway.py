from abc import ABC, abstractmethod

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.domain.ctx.user.entity import UserEntity


class IntervalGateway(ABC):

    @abstractmethod
    async def start(self, user: UserEntity, category_uuid: CategoryId, started_at: int) -> IntervalStartDTO: ...

    @abstractmethod
    async def stop(self, user: UserEntity, category_uuid: CategoryId, stopped_at: int) -> IntervalStopDTO: ...

    @abstractmethod
    async def clear(self, user: UserEntity, category_uuid: CategoryId) -> IntervalClearDTO: ...
