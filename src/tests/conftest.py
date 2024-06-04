from collections.abc import AsyncGenerator
import pytest_asyncio
from dishka import AsyncContainer
from src.infrastructure.di.container import build_container

@pytest_asyncio.fixture(scope="session")
async def di() -> AsyncGenerator[AsyncContainer, None]:
    container = build_container()
    yield container
    await container.close()