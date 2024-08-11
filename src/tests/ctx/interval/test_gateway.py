from datetime import datetime

import pytest

from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.gateway import IntervalGateway
from src.domain.ctx.user.entity import UserEntity
from src.tests.conftest import dl, fx_user, gateway_interval
from src.tests.dataloader import Dataloader


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_stop_ok -v -s
async def test_interval_stop_ok(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    print()
    # Arrange

    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    target_interval = await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid)

    # Act
    res = await gateway_interval.stop(user=fx_user, category_uuid=CategoryId(category.uuid))

    # Assert
    assert res.user_uuid == fx_user.uuid
    assert res.category_uuid == category.uuid
    assert res.interval_uuid == target_interval.uuid


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_stop_category_not_found_err -v -s
async def test_interval_stop_category_not_found_err(fx_user: UserEntity, gateway_interval: IntervalGateway):
    # Arrange
    category_uuid_not_exist = CategoryId("-1")

    # Assert
    with pytest.raises(EntityNotFound) as err:
        await gateway_interval.stop(user=fx_user, category_uuid=category_uuid_not_exist)
    assert category_uuid_not_exist in str(err.value)


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_stop_not_updated -v -s
async def test_interval_stop_not_updated(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    print()
    # Arrange
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)

    mock_category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=mock_category.uuid)

    # Assert
    with pytest.raises(EntityNotFound) as err:
        await gateway_interval.stop(user=fx_user, category_uuid=CategoryId(category.uuid))
    assert f"{category.uuid}" in str(err.value)


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_start_ok -v -s
async def test_interval_start_ok(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    print()
    # Arrange
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)

    await dl.category_loader.create(user_uuid=fx_user.uuid)

    # Act
    res = await gateway_interval.start(user=fx_user, category_uuid=CategoryId(category.uuid))

    # Assert
    assert res.category_uuid == category.uuid
    assert res.interval_uuid
    assert res.user_uuid == fx_user.uuid


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_start_started_interval_already_exist -v -s
async def test_interval_start_started_interval_already_exist(
    dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway
):
    print()
    # Arrange
    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    started_at = int(datetime.now().timestamp())

    await dl.category_loader.create(user_uuid=fx_user.uuid)
    mock_timestamp = started_at - 10
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=mock_timestamp)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=started_at)

    # Act
    res = await gateway_interval.start(user=fx_user, category_uuid=CategoryId(category.uuid))

    # Assert
    fltr = {"category_uuid": category.uuid, "user_uuid": fx_user.uuid, "end_at": {"$eq": None}}
    started_intervals_list = await dl.interval_loader.get_lst(fltr=fltr)
    assert len(started_intervals_list) == 1
    assert res.category_uuid == category.uuid
    assert res.interval_uuid
    assert res.user_uuid == fx_user.uuid


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_start_category_not_find -v -s
async def test_interval_start_category_not_find(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    # Arrange
    category_id_not_exist = CategoryId("-1")

    # Assert
    with pytest.raises(EntityNotFound) as err:
        await gateway_interval.start(user=fx_user, category_uuid=category_id_not_exist)
    assert category_id_not_exist in str(err.value)
