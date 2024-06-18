from abc import ABC, abstractmethod

from src.domain.ctx.user.interface.types import UserId


class UserGateway(ABC):

    @abstractmethod
    async def is_exist(self, uuid: UserId) -> bool: ...
