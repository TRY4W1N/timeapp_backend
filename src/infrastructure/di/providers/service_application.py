from dishka import Provider, Scope, provide

from src.application.service.auth.firebase.service import AuthServiceFirebase
from src.domain.ctx.auth.dto import UserIdentityDTO
from src.domain.ctx.auth.interface.service import AuthService
from src.domain.exception.base import AuthError
from src.infrastructure.di.alias import ConfigType


class AppServiceProvider(Provider):
    component = "SERVICE_APPLICATION"

    @provide(scope=Scope.APP)
    async def get_auth_service(self, config: ConfigType) -> AuthService:
        service = AuthServiceFirebase(name=config.APP_NAME, secret_path=config.FIREBASE_SECRET_PATH)
        service.setup()

        if config.APP_ENV == "DEV":

            async def get_by_token_mocked(token: str) -> UserIdentityDTO:
                if token not in config.DEV_USERS:
                    raise AuthError(msg="Error on verify token")
                user_dev_data = config.DEV_USERS[token]
                return UserIdentityDTO(
                    id=user_dev_data["id"],
                    name=user_dev_data["name"],
                    email=user_dev_data["email"],
                )

            service.get_by_token = get_by_token_mocked

        return service
