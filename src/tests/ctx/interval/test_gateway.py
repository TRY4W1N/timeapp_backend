from datetime import datetime, timedelta

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
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid)  # duplicate of target
    target_interval = await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category.uuid)

    # Act
    res = await gateway_interval.stop(user=fx_user, category_uuid=CategoryId(category.uuid))

    # Assert
    assert res.user_uuid == fx_user.uuid
    assert res.category_uuid == category.uuid
    assert res.interval_uuid == target_interval.uuid


# pytest src/tests/ctx/interval/test_gateway.py::test_interval_stop_with_many_opened -v -s
async def test_interval_stop_with_many_opened(dl: Dataloader, fx_user: UserEntity, gateway_interval: IntervalGateway):
    print()
    # Arrange

    category = await dl.category_loader.create(user_uuid=fx_user.uuid)
    started_at = datetime.now() - timedelta(hours=1, minutes=2)
    started_at_day2ago = started_at - timedelta(days=2) - timedelta(hours=1, minutes=2)
    started_at_day5ago = started_at - timedelta(days=5) - timedelta(hours=2, minutes=15)

    await dl.interval_loader.create(
        user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=int(started_at_day5ago.timestamp())
    )
    await dl.interval_loader.create(
        user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=int(started_at_day2ago.timestamp())
    )
    await dl.interval_loader.create(
        user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=int(started_at.timestamp())
    )  # duplicate of target
    target_interval = await dl.interval_loader.create(
        user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=int(started_at.timestamp())
    )

    # Act
    res = await gateway_interval.stop(user=fx_user, category_uuid=CategoryId(category.uuid))
    # Assert
    fltr = {"category_uuid": category.uuid, "user_uuid": fx_user.uuid}
    all_interval_list = await dl.interval_loader.get_lst(fltr=fltr)
    assert len(all_interval_list) == 8
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
    await dl.category_loader.create(user_uuid=fx_user.uuid)

    started_at = datetime.now()
    started_at_day2ago = started_at - timedelta(days=2) - timedelta(hours=1, minutes=2)
    started_at_day5ago = started_at - timedelta(days=5) - timedelta(hours=2, minutes=15)

    await dl.interval_loader.create(
        user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=int(started_at_day5ago.timestamp())
    )
    await dl.interval_loader.create(
        user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=int(started_at_day2ago.timestamp())
    )
    await dl.interval_loader.create(
        user_uuid=fx_user.uuid, category_uuid=category.uuid, started_at=int(started_at.timestamp())
    )

    # Act
    res = await gateway_interval.start(user=fx_user, category_uuid=CategoryId(category.uuid))
    # State on start is:
    #   interval_58791f11-d218-4db4-bc3e-823bf6fe29bb 2024-08-09 17:34:29 - None
    #   interval_739bb075-d1e1-4f9d-b453-6fefc29309e5 2024-08-12 18:47:29 - None
    #   interval_2ffe4fa1-b95c-437a-976e-35d8f09709a9 2024-08-14 19:49:29 - None
    # We see, 3 intervals not closed for target category
    #
    # State after add new interval with OLD NOT CLOSED INTERVALS:
    #   interval_58791f11-d218-4db4-bc3e-823bf6fe29bb 2024-08-09 17:34:29 - 2024-08-10 00:00:00 <-- changed old
    #   6d2b9232-507a-4c37-992c-9efed1c2a6b2 2024-08-10 00:00:00 - 2024-08-11 00:00:00 <-- new
    #   823a6ad2-1255-47e5-843e-0d433b7739b1 2024-08-11 00:00:00 - 2024-08-12 00:00:00 <-- new
    #   c5d5d193-5ac4-44f9-9881-99baf3258f0e 2024-08-12 00:00:00 - 2024-08-12 18:47:29 <-- new
    #   interval_739bb075-d1e1-4f9d-b453-6fefc29309e5 2024-08-12 18:47:29 - 2024-08-13 00:00:00 <-- changed old
    #   e44aabb4-ea9d-4e6f-bbe3-cfc91003e2af 2024-08-13 00:00:00 - 2024-08-14 00:00:00 <-- new
    #   7d5af201-cfad-40c1-a045-adde599d6eff 2024-08-14 00:00:00 - 2024-08-14 19:49:29 <-- new
    #   interval_2ffe4fa1-b95c-437a-976e-35d8f09709a9 2024-08-14 19:49:29 - 2024-08-14 19:49:29 <-- changed old
    # We closed intervals by start next interval
    # And this new intervals we was split by day

    # Assert
    fltr = {"category_uuid": category.uuid, "user_uuid": fx_user.uuid, "end_at": {"$eq": None}}
    started_interval_list = await dl.interval_loader.get_lst(fltr=fltr)
    fltr = {"category_uuid": category.uuid, "user_uuid": fx_user.uuid}
    all_interval_list = await dl.interval_loader.get_lst(fltr=fltr)
    # Old 3 not closed intervals transform to 8 intervals + 1 new open interval from current time
    assert len(all_interval_list) == 9
    assert len(started_interval_list) == 1
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
