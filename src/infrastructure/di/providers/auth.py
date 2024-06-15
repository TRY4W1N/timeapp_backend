from dishka import Provider, Scope, provide

from src.domain.ctx.auth.dto import UserIdentity
from src.domain.exeption.base import AuthError
from src.infrastructure.di.alias import AuthType


class ServiceProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def get_user(self, auth: AuthType, database: DatabaseMongoType,  token: str, check_revoked) -> UserIdentity:
        try:
            user_identify = await auth.get_user_by_token(token=token, check_revoked=check_revoked)
        except Exception as e:
            raise AuthError(msg=f"User not found by token: {e}") from e

        return user