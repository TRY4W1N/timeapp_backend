from abc import ABC, abstractmethod

from src.application.service.auth.dto import UserIdentity


class AuthGateway(ABC):
    @abstractmethod
    async def get_user_by_token(self, token: str, check_revoked: bool = True) -> UserIdentity: ...
