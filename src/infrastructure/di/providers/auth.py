from dishka import Provider, Scope, provide

from src.application.settings import settings
from src.domain.ctx.auth.firebase.application import FirebaseApplication, FirebaseApplicationSingleton
from src.domain.ctx.auth.firebase.interface.gateway import IFirebaseApplication
from src.domain.ctx.auth.gateway import AuthGateway
from src.domain.ctx.auth.interface.auth_provider_interface import IAuthGateway


class AppServiceProvider(Provider):
    component = "AUTH"

    @provide(scope=Scope.APP)
    async def get_auth_provider(
        self,
    ) -> IAuthGateway:
        firebase_app = FirebaseApplicationSingleton(
            name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH
        )
        firebase_app.setup()
        return AuthGateway(firebase_app=firebase_app)

    @provide(scope=Scope.APP)
    async def get_firebase_app_singleton(
        self,
    ) -> FirebaseApplicationSingleton:
        return FirebaseApplicationSingleton(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)

    @provide(scope=Scope.REQUEST)
    async def get_firebase_app(
        self,
    ) -> IFirebaseApplication:
        return FirebaseApplication(name=settings.FIREBASE_APP_NAME, secret_path=settings.FIREBASE_SECRET_PATH)
