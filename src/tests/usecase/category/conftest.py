from collections.abc import AsyncGenerator

import pytest
from dishka import AsyncContainer

from src.domain.usecases.category.create import UsecaseCategoryCreate
from src.domain.usecases.category.delete import UsecaseCategoryDelete
from src.domain.usecases.category.get_list import UsecaseCategoryGetList
from src.domain.usecases.category.update import UsecaseCategoryUpdate


@pytest.fixture(scope="function")
async def usecase_category_create(dicon: AsyncContainer) -> AsyncGenerator[UsecaseCategoryCreate, None]:
    yield await dicon.get(UsecaseCategoryCreate, component="USECASE")


@pytest.fixture(scope="function")
async def usecase_category_delete(dicon: AsyncContainer) -> AsyncGenerator[UsecaseCategoryDelete, None]:
    yield await dicon.get(UsecaseCategoryDelete, component="USECASE")


@pytest.fixture(scope="function")
async def usecase_category_update(dicon: AsyncContainer) -> AsyncGenerator[UsecaseCategoryUpdate, None]:
    yield await dicon.get(UsecaseCategoryUpdate, component="USECASE")


@pytest.fixture(scope="function")
async def usecase_category_get_list(dicon: AsyncContainer) -> AsyncGenerator[UsecaseCategoryGetList, None]:
    yield await dicon.get(UsecaseCategoryGetList, component="USECASE")
