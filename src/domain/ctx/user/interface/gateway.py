from abc import ABC, abstractmethod


class UserGateway(ABC):

    @abstractmethod
    async def is_exist(self, uuid: str) -> bool: ...
