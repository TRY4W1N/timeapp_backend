import pytest

from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.time_all.interface.gateway import TimeAllGateway
from src.domain.ctx.user.entity import UserEntity
from src.tests.dataloader import Dataloader


# pytest src/tests/ctx/timeall/test_time_all.py::test_cat_lst -v -s
async def test_get_category_statistic_ok(dl: Dataloader, fx_user: UserEntity, gateway_time_all: TimeAllGateway):
    print()
    # Arrange

    # Category 1 with total time 0 (without intervals and time_all records)
    category_1 = await dl.category_loader.create(user_uuid=fx_user.uuid)
    category_1_total_time = 0

    # Category 2 open interval with closed intervals
    category_2 = await dl.category_loader.create(user_uuid=fx_user.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_2.uuid, started_at=2000)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_2.uuid, started_at=10, end_at=30)
    await dl.time_all_loader.create(user_uuid=fx_user.uuid, category_uuid=category_2.uuid, total_time=1000)
    category_2_total_time = 1020

    # Category 3 only closed intervals
    category_3 = await dl.category_loader.create(user_uuid=fx_user.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_3.uuid, started_at=10, end_at=30)
    await dl.time_all_loader.create(user_uuid=fx_user.uuid, category_uuid=category_3.uuid, total_time=200)
    category_3_total_time = 220

    arrange_category_set_uuid = set([category_3.uuid, category_2.uuid, category_1.uuid])
    arrange_time_all_categories = {
        category_1.uuid: category_1_total_time,
        category_2.uuid: category_2_total_time,
        category_3.uuid: category_3_total_time,
    }

    # Act
    res = await gateway_time_all.get_categories_statistic(user=fx_user)

    # Assert
    res_percent_sum = sum((time_percent.time_percent for time_percent in res.category_list), 0)
    res_category_set_uuid = {category.category_uuid for category in res.category_list}
    res_time_all_categories = {category.category_uuid: category.total_time for category in res.category_list}

    assert res_percent_sum == 100
    assert res_category_set_uuid == arrange_category_set_uuid
    assert res_time_all_categories == arrange_time_all_categories
    assert res.user_uuid == fx_user.uuid


# pytest src/tests/ctx/timeall/test_time_all.py::test_get_categories_statistic -v -s
async def test_get_category_statistic_category_not_found(
    dl: Dataloader, fx_user: UserEntity, gateway_time_all: TimeAllGateway
):
    print()
    # Act
    with pytest.raises(EntityNotFound) as err:
        await gateway_time_all.get_categories_statistic(user=fx_user)
    # Assert
    assert f"{fx_user.uuid}" in str(err.value)


# pytest src/tests/ctx/timeall/test_time_all.py::test_get_category_statistic_categories_total_time_0 -v -s
async def test_get_category_statistic_categories_total_time_0(
    dl: Dataloader, fx_user: UserEntity, gateway_time_all: TimeAllGateway
):
    print()
    # Arrange
    category_counter = 4
    _ = [await dl.category_loader.create(user_uuid=fx_user.uuid) for _ in range(category_counter)]
    time_percent_every_category = category_counter / 100
    # Act

    res = await gateway_time_all.get_categories_statistic(user=fx_user)

    # Assert
    assert res.user_uuid == fx_user.uuid
    category_set_time_percent = [category.time_percent for category in res.category_list]
    for category_time_percent in category_set_time_percent:
        assert category_time_percent == time_percent_every_category
