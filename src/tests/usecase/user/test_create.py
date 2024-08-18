from unittest.mock import AsyncMock, patch

import pytest

from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.auth.dto import UserIdentityDTO
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.usecases.user.user_get_by_token import UsecaseUserGetByToken
from src.infrastructure.config import ConfigBase
from src.tests.dataloader import Dataloader


async def _get_fake_user_and_token_from_config(dicon) -> tuple[UserIdentityDTO, str]:
    config = await dicon.get(ConfigBase, component="CONFIG")
    user = UserIdentityDTO(
        id=config.DEV_USERS["aboba_token"]["id"],
        name=config.DEV_USERS["aboba_token"]["name"],
        email=config.DEV_USERS["aboba_token"]["email"],
    )
    token = config.DEV_USERS["aboba_token"]["token"]
    return user, token


# pytest src/tests/usecase/user/test_create.py::test_user_found -vv -s
@pytest.mark.parametrize("user_mock", [_get_fake_user_and_token_from_config])
@patch.object(UserGateway, "get", new_callable=AsyncMock)
async def test_user_found(mock_get, usecase_user_get_by_token: UsecaseUserGetByToken, dicon, user_mock):
    # Arrange
    user, token = await user_mock(dicon)

    auth_service = AsyncMock()
    auth_service.get_by_token.return_value = user

    mock_get.side_effect = user

    # Act
    res = await usecase_user_get_by_token.execute(token=token)

    # Assert
    assert res.email == user.email
    assert res.name == user.name
    assert res.uuid == user.id


# pytest src/tests/usecase/user/test_create.py::test_user_not_found -vv -s
@pytest.mark.parametrize("arrange_func", [_get_fake_user_and_token_from_config])
@patch.object(UserGateway, "get", new_callable=AsyncMock)
async def test_user_not_found(
    mock_get, dl: Dataloader, usecase_user_get_by_token: UsecaseUserGetByToken, dicon, arrange_func
):
    # Arrange
    user, token = await arrange_func(dicon)

    auth_service = AsyncMock()
    auth_service.get_by_token.return_value = user

    mock_get.side_effect = EntityNotFound

    # Act
    res = await usecase_user_get_by_token.execute(token=token)

    # Assert
    assert res.email == user.email
    assert res.name == user.name
    assert res.uuid == user.id
