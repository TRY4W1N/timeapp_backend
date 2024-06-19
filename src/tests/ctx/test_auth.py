from dishka import AsyncContainer
import pytest

from src.domain.ctx.auth.interface.auth_provider_gateway import IAuthGateway
from src.domain.exception.base import AuthError
from src.tests.fixtures.auth import mock_app_service_container


# pytest src/tests/ctx/test_auth.py::test_token_error -v -s
async def test_token_error(di: AsyncContainer):
    token = "aboba"
    async with di() as container:
        auth = await container.get(IAuthGateway, component="AUTH")
        with pytest.raises(AuthError) as err:
            await auth.get_user_by_token(token=token)
        assert "Error on verify token" in str(err.value)
    

# pytest src/tests/ctx/test_auth.py::test_some -v -s
async def test_some(mock_app_service_container):
    user_id = "aboba_id"
    container = await mock_app_service_container.get(IAuthGateway, component="AUTH")
    with pytest.raises(AuthError) as e:
        await container.get_user_by_token(token="aboba")
    assert f"Error on get user by id={user_id}: Not setup"