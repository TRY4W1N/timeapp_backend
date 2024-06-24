from dishka import Provider, Scope, provide

from src.application.service.auth.firebase.service import AuthServiceFirebase
from src.domain.ctx.auth.interface.service import AuthService
from src.infrastructure.di.alias import ConfigType


class AppServiceProvider(Provider):
    component = "SERVICE_APPLICATION"

    @provide(scope=Scope.APP)
    async def get_auth_service(self, config: ConfigType) -> AuthService:
        service = AuthServiceFirebase(name=config.APP_NAME, secret_path=config.FIREBASE_SECRET_PATH)
        service.setup()
        return service
