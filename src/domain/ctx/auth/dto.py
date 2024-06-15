from dataclasses import dataclass

from src.domain.ctx.auth.enum import AuthProviderEnum


@dataclass
class TokenIdentity:
    user_id: str
    name: str
    email: str
    email_verified: bool
    pic: str
    auth_time: int
    provider: str
    provider_data: dict
    iss: str
    aud: str
    uid: str
    iat: int
    exp: int


@dataclass
class ProviderIdentity:
    type: AuthProviderEnum
    data: dict


@dataclass
class UserIdentity:
    id: str
    name: str
    active: bool
    pic: str
    email: str
    email_verified: bool
    provider: ProviderIdentity
