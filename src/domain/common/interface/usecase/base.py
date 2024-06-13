from abc import ABC, abstractmethod


class Usecase(ABC):

    @abstractmethod
    async def execute(self, *args, **kwargs): ...
