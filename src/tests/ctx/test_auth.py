import pytest
from dishka import AsyncContainer

from src.application.service.auth.interface.gateway import AuthGateway
from src.domain.exception.base import AuthError
from src.tests.conftest import mock_app_service_container


# pytest src/tests/ctx/test_auth.py::test_token_error -v -s
async def test_token_error(dicon: AsyncContainer):
    # Arrange
    token = "aboba"

    # Act
    async with dicon() as container:
        auth = await container.get(AuthGateway, component="APPLICATION_SERVICE")
        with pytest.raises(AuthError) as err:
            await auth.get_user_by_token(token=token)
        # Assert
        assert "Error on verify token" in str(err.value)


# pytest src/tests/ctx/test_auth.py::test_some -v -s
async def test_some(mock_app_service_container):
    # Arrange

    user_id = "aboba_id"

    # Act
    container = await mock_app_service_container.get(AuthGateway, component="APPLICATION_SERVICE")
    with pytest.raises(AuthError) as e:
        await container.get_user_by_token(token="aboba")

    # Assert
    assert f"Error on get user by id={user_id}: Not setup"
