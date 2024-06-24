from abc import ABC, abstractmethod

from src.domain.ctx.user.dto import UserCreateDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.ctx.user.interface.types import UserId


class UserGateway(ABC):

    @abstractmethod
    async def is_exist(self, uuid: UserId) -> bool: ...

    @abstractmethod
    async def get(self, uuid: UserId) -> UserEntity: ...

    @abstractmethod
    async def create(self, user: UserCreateDTO) -> UserEntity: ...
