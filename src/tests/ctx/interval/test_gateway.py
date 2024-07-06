from datetime import datetime

import pytest

from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.entity import UserEntity
from src.domain.exception.base import DocumentNotUpdated
from src.tests.conftest import dl, fx_user, gateway_interval
from src.tests.dataloader import Dataloader


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_stop_ok -v -s
async def test_interval_stop_ok(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    # Arrange
    stopped_at = datetime.now()
    timestamp = int(round(stopped_at.timestamp()))
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    target_interval = await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid)

    # Act
    res = await gateway_interval.stop(user=fx_user, category_uuid=CategoryId(category.uuid), stopped_at=timestamp)

    # Assert
    assert res.user_uuid == fx_user.uuid
    assert res.category_uuid == CategoryId(category.uuid)
    assert res.interval_uuid == IntervalId(target_interval.uuid)


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_stop_category_not_found_err -v -s
async def test_interval_stop_category_not_found_err(fx_user: UserEntity, gateway_interval: IntervalGateway):
    # Arrange
    category_uuid_not_exist = CategoryId("-1")
    stopped_at = datetime.now()
    timestamp = int(round(stopped_at.timestamp()))

    # Assert
    with pytest.raises(EntityNotFound) as err:
        await gateway_interval.stop(user=fx_user, category_uuid=category_uuid_not_exist, stopped_at=timestamp)
    assert f"{category_uuid_not_exist=}" in str(err.value)


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_stop_not_updated -v -s
async def test_interval_stop_not_updated(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    # Arrange
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    stopped_at = datetime.now()
    timestamp = int(round(stopped_at.timestamp()))

    mock_category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=mock_category.uuid)

    # Assert
    with pytest.raises(DocumentNotUpdated) as err:
        await gateway_interval.stop(user=fx_user, category_uuid=CategoryId(category.uuid), stopped_at=timestamp)
    assert f"{category.uuid}" in str(err.value)


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_clear_ok -v -s
@pytest.mark.parametrize("arrange_interval_count", [0, 5])
async def test_interval_clear_ok(
    dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway, arrange_interval_count: int
):
    # Arrange
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    _ = [
        await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid)
        for _ in range(arrange_interval_count)
    ]

    mock_category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=CategoryId(mock_category.uuid))

    # Act
    res = await gateway_interval.clear(user=fx_user, category_uuid=CategoryId(category.uuid))

    # Assert
    assert res.category_uuid == CategoryId(category.uuid)
    assert res.interval_count == arrange_interval_count
    assert res.user_uuid == fx_user.uuid


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_start_ok -v -s
async def test_interval_start_ok(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    # Arrange
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    started_at = datetime.now()
    timestamp = int(round(started_at.timestamp()))

    await dl.category_loader.create(user_uuid=fx_user.uuid)

    # Act
    res = await gateway_interval.start(user=fx_user, category_uuid=CategoryId(category.uuid), started_at=timestamp)

    # Assert
    assert res.category_uuid == CategoryId(category.uuid)
    assert res.interval_uuid
    assert res.user_uuid == fx_user.uuid


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_start_multiple_request_at_the_same_time -v -s
async def test_interval_start_multiple_request_at_the_same_time(
    dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway
):
    # Arrange
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    started_at = datetime.now()
    timestamp = int(round(started_at.timestamp()))

    mokc_timestamp = timestamp + 100

    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=mokc_timestamp)

    # Act
    res = await gateway_interval.start(user=fx_user, category_uuid=CategoryId(category.uuid), started_at=timestamp)
    await gateway_interval.start(user=fx_user, category_uuid=CategoryId(category.uuid), started_at=timestamp)
    await gateway_interval.start(user=fx_user, category_uuid=CategoryId(category.uuid), started_at=timestamp)

    # Assert
    # Only one record was added during the multi-query requests
    interval_fltr = {
        "user_uuid": fx_user.uuid,
        "category_uuid": category.uuid,
        "started_at": timestamp,
    }
    count_added_intervals = await dl.interval_loader.get_lst(fltr=interval_fltr)
    assert len(count_added_intervals) == 1
    assert res.category_uuid == CategoryId(category.uuid)
    assert res.interval_uuid
    assert res.user_uuid == fx_user.uuid

    # Check that other records exist
    fltr = {
        "user_uuid": fx_user.uuid,
        "category_uuid": category.uuid,
    }
    count_all_intervals = await dl.interval_loader.get_lst(fltr=fltr)
    assert len(count_all_intervals) > len(count_added_intervals)


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_start_category_not_find -v -s
async def test_interval_start_category_not_find(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    # Arrange
    category_id_not_exist = CategoryId("-1")
    started_at = datetime.now()
    timestamp = int(round(started_at.timestamp()))

    # Assert
    with pytest.raises(EntityNotFound) as err:
        await gateway_interval.start(user=fx_user, category_uuid=category_id_not_exist, started_at=timestamp)
    assert category_id_not_exist in str(err.value)
