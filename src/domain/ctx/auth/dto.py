from dataclasses import dataclass


@dataclass
class UserIdentityDTO:
    id: str
    name: str
    email: str
