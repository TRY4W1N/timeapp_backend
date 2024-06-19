from src.domain.ctx.auth.dto import UserIdentity
from src.domain.ctx.auth.firebase.interface.gateway import IFirebaseApplicationGateway
from src.domain.ctx.auth.interface.auth_provider_gateway import IAuthGateway
from src.domain.exception.base import AuthError


class AuthGateway(IAuthGateway):
    def __init__(self, firebase_app: IFirebaseApplicationGateway) -> None:
        self._fb_app = firebase_app

    async def get_user_by_token(self, token: str, check_revoked: bool = True) -> UserIdentity:
        try:
            token_identity = await self._fb_app.verify_token(token=token, check_revoked=check_revoked)
        except Exception as e:
            raise AuthError(msg=f"Error on verify token: {e}") from e
        try:
            user_identity = await self._fb_app.get_user(id=token_identity.user_id)
        except Exception as e:
            raise AuthError(msg=f"Error on get user by id={token_identity.user_id}: {e}") from e
        return user_identity
