from collections.abc import AsyncGenerator

import pytest
from dishka import AsyncContainer

from src.domain.usecases.category.add import UsecaseCategoryAdd


@pytest.fixture(scope="function")
async def usecase_category_add(dicon: AsyncContainer) -> AsyncGenerator[UsecaseCategoryAdd, None]:
    yield await dicon.get(UsecaseCategoryAdd, component="USECASE")
