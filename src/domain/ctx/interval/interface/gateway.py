from abc import ABC, abstractmethod

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.dto import IntervalStartDTO, IntervalStopDTO
from src.domain.ctx.user.entity import UserEntity


class IntervalGateway(ABC):

    @abstractmethod
    async def start(self, user: UserEntity, category_uuid: CategoryId) -> IntervalStartDTO: ...

    @abstractmethod
    async def stop(self, user: UserEntity, category_uuid: CategoryId) -> IntervalStopDTO: ...
