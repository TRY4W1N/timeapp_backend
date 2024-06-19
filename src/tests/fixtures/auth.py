from unittest.mock import Mock
from dishka import Provider, Scope, make_async_container, provide
import pytest_asyncio

from src.domain.ctx.auth.firebase.application import FirebaseApplicationGateway
from src.domain.ctx.auth.gateway import AuthGateway
from src.domain.ctx.auth.interface.auth_provider_gateway import IAuthGateway
from src.tests.fixtures.common.mock_functions import mock_verify_token_random_user_id


@pytest_asyncio.fixture
async def mock_app_service_container():
    container = make_async_container(MockAppServiceProvider())
    yield container
    await container.close()



class MockAppServiceProvider(Provider):
    component = "AUTH"

    @provide(scope=Scope.APP)
    async def get_auth_provider(
        self,
    ) -> IAuthGateway:
        mock = Mock()
        mock.return_value = mock_verify_token_random_user_id

        firebase = FirebaseApplicationGateway(name="Some", secret_path="some")
        firebase.verify_token = mock()
        return AuthGateway(firebase_app=firebase)