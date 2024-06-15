from dataclasses import dataclass


@dataclass
class UserEntity:
    uuid: str
    name: str
    email: str
