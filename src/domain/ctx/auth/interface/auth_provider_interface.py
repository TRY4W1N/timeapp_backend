from abc import ABC, abstractmethod

from src.domain.ctx.auth.dto import UserIdentity


class IAuthGateway(ABC):
    @abstractmethod
    async def get_user_by_token(self, token: str, check_revoked: bool = True) -> UserIdentity:
        ...
