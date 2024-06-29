import pytest
from dishka import AsyncContainer

from src.domain.ctx.auth.interface.service import AuthService
from src.domain.exception.base import AuthError


# pytest src/tests/ctx/test_auth.py::test_token_error -v -s
async def test_token_error(dicon: AsyncContainer):
    # Arrange
    token = "aboba"

    # Act
    async with dicon() as container:
        auth = await container.get(AuthService, component="SERVICE_APPLICATION")
        with pytest.raises(AuthError) as err:
            await auth.get_by_token(token=token)
        # Assert
        assert "Error on verify token" in str(err.value)
