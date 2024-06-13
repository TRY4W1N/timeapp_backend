from abc import ABC, abstractmethod


class Usecase(ABC):

    @abstractmethod
    def execute(self, *args, **kwargs): ...
