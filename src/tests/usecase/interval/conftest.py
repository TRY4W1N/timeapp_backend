from collections.abc import AsyncGenerator

import pytest
from dishka import AsyncContainer

from src.domain.usecases.interval.track_start import UsecaseIntervalTrackStart
from src.domain.usecases.interval.track_stop import UsecaseIntervalTrackStop


@pytest.fixture(scope="function")
async def usecase_interval_track_start(dicon: AsyncContainer) -> AsyncGenerator[UsecaseIntervalTrackStart, None]:
    yield await dicon.get(UsecaseIntervalTrackStart, component="USECASE")


@pytest.fixture(scope="function")
async def usecase_interval_track_stop(dicon: AsyncContainer) -> AsyncGenerator[UsecaseIntervalTrackStop, None]:
    yield await dicon.get(UsecaseIntervalTrackStop, component="USECASE")
