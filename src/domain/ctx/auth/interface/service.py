from abc import ABC, abstractmethod

from src.domain.ctx.auth.dto import UserIdentityDTO


class AuthService(ABC):

    @abstractmethod
    async def get_by_token(self, token: str) -> UserIdentityDTO: ...
