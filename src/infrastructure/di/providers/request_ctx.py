from dishka import Provider, Scope, from_context, provide
from fastapi import Request

from src.domain.ctx.user.entity import UserEntity
from src.infrastructure.di.alias import UserToken


class RequestProvider(Provider):
    component = "REQUEST"

    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    def get_token(self, request: Request) -> UserToken:
        return UserToken(request.headers.get("Authorization") or "")

    @provide(scope=Scope.REQUEST)
    async def get_user(self, token: UserToken) -> UserEntity:
        print(f"Token={token}, but ignored..")
        return UserEntity(uuid="not_uuid", name="jayse", email="aboba@gmail.com")
