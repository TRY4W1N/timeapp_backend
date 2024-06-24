from unittest.mock import Mock

from dishka import Provider, Scope, provide

from src.application.service.auth.dto import TokenIdentity
from src.application.service.auth.interface.gateway import AuthGateway
from src.infrastructure.auth.gateway.auth import AuthGatewayFirebase
from src.infrastructure.auth.gateway.firebase import FirebaseGatewayImplement


async def mock_verify_token_random_user_id(token: str, check_revoked: bool = True) -> TokenIdentity:
    return TokenIdentity(
        user_id="aboba_id",
        name="test",
        email="test",
        email_verified=True,
        pic="test",
        auth_time=1337,
        iss="test",
        aud="test",
        uid="test",
        provider="google.com",
        provider_data={},
        iat=1337,
        exp=1337,
    )


class MockAppServiceProvider(Provider):
    component = "APPLICATION_SERVICE"

    @provide(scope=Scope.APP)
    async def get_auth_provider(
        self,
    ) -> AuthGateway:
        mock = Mock()
        mock.return_value = mock_verify_token_random_user_id

        firebase = FirebaseGatewayImplement(name="Some", secret_path="some")
        firebase.verify_token = mock()
        return AuthGatewayFirebase(firebase_app=firebase)
