import pytest

from src.domain.ctx.auth.interface.service import AuthService
from src.domain.usecases.user.user_get_by_token import UsecaseUserGetByToken
from src.infrastructure.config import ConfigBase


# pytest src/tests/usecase/user/test_create.py::test_user_create -vv -s
async def test_user_create(mocker, usecase_user_get_by_token: UsecaseUserGetByToken, dicon):
    # Arrange
    fake_token = "aboba_token"
    config = await dicon.get(ConfigBase, component="CONFIG")
    print(f"{config.DEV_USERS=}")
    # Act
    res = await usecase_user_get_by_token.execute(token=fake_token)

    assert res
