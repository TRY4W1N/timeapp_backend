from dataclasses import dataclass

from src.domain.ctx.user.interface.types import UserId


@dataclass
class UserCreateDTO:
    uuid: UserId
    name: str
    email: str
