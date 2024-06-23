from abc import ABC, abstractmethod

from src.application.service.auth.dto import TokenIdentity, UserIdentity


class FirebaseGateway(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def is_setup(self) -> bool: ...

    @abstractmethod
    def setup(self) -> None: ...

    @abstractmethod
    async def verify_token(self, token: str, check_revoked: bool = True) -> TokenIdentity: ...

    @abstractmethod
    async def get_user(self, id: str) -> UserIdentity: ...
