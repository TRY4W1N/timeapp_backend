from collections.abc import AsyncGenerator

import pytest
from dishka import AsyncContainer

from src.domain.usecases.user.user_get_by_token import UsecaseUserGetByToken


@pytest.fixture(scope="function")
async def usecase_user_get_by_token(dicon: AsyncContainer) -> AsyncGenerator[UsecaseUserGetByToken, None]:
    yield await dicon.get(UsecaseUserGetByToken, component="USECASE")
