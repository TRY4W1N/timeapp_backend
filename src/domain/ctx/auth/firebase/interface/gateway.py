from abc import ABC, abstractmethod

from src.domain.ctx.auth.dto import TokenIdentity, UserIdentity


class IFirebaseApplication(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def is_setup(self) -> bool:
        ...

    @abstractmethod
    def setup(self) -> None:
        ...

    @abstractmethod
    async def verify_token(self, token: str, check_revoked: bool = True) -> TokenIdentity:
        ...

    @abstractmethod
    async def get_user(self, id: str) -> UserIdentity:
        ...
