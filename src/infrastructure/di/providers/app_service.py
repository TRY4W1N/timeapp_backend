from dishka import Provider, Scope, provide

from src.domain.ctx.auth.interface.gateway import AuthGateway
from src.infrastructure.auth.gateway.auth import AuthGatewayFirebase
from src.infrastructure.auth.gateway.firebase import FirebaseGatewayImplement
from src.infrastructure.di.alias import ConfigType



class AppServiceProvider(Provider):
    component = "APPLICATION_SERVICE"

    @provide(scope=Scope.APP)
    async def get_auth_provider(
        self, config: ConfigType
    ) -> AuthGateway:
        firebase_app = FirebaseGatewayImplement(
            name=config.APP_NAME, secret_path=config.FIREBASE_SECRET_PATH
        )
        firebase_app.setup()
        return AuthGatewayFirebase(firebase_app=firebase_app)
