from dishka import Provider, Scope, provide

from src.application.settings import settings
from src.domain.ctx.auth.firebase.application import FirebaseApplicationGateway
from src.domain.ctx.auth.gateway import AuthGateway
from src.domain.ctx.auth.interface.auth_provider_gateway import IAuthGateway


class AppServiceProvider(Provider):
    component = "APPLICATION_SERVICE"

    @provide(scope=Scope.APP)
    async def get_auth_provider(
        self,
    ) -> IAuthGateway:
        firebase_app = FirebaseApplicationGateway(
            name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH
        )
        firebase_app.setup()
        return AuthGateway(firebase_app=firebase_app)
