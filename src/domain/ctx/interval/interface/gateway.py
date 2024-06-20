from abc import ABC, abstractmethod

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import (
    IntervalClearDTO,
    IntervalStartDTO,
    IntervalStopDTO,
)
from src.domain.ctx.user.interface.types import UserId


class IntervalGateway(ABC):

    @abstractmethod
    async def start(self, user_uuid: UserId, category_uuid: CategoryId) -> IntervalStartDTO: ...

    @abstractmethod
    async def stop(self, user_uuid: UserId, category_uuid: CategoryId) -> IntervalStopDTO: ...

    @abstractmethod
    async def clear(self, user_uuid: UserId, category_uuid: CategoryId) -> IntervalClearDTO: ...
