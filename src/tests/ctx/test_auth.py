from dishka import AsyncContainer
import pytest

from src.domain.ctx.auth.interface.auth_provider_interface import IAuthGateway
from src.domain.exeption.base import AuthError


# pytest src/tests/tmain/repository/test_auth.py::test_token_error -v -s
async def test_token_error(di: AsyncContainer):
    token = "aboba"
    async with di() as container:
        auth = await container.get(IAuthGateway, component="AUTH")
        with pytest.raises(AuthError) as err:
            await auth.get_user_by_token(token=token)
        assert "Error on verify token" in str(err.value)
