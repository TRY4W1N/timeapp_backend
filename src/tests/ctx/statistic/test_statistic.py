import pytest

from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.statistic.interface.gateway import StatisticGateway
from src.domain.ctx.user.entity import UserEntity
from src.tests.dataloader import Dataloader


# pytest src/tests/ctx/statistic/test_statistic.py::test_get_category_statistic_ok -v -s
async def test_get_category_statistic_ok(dl: Dataloader, fx_user: UserEntity, gateway_time_all: StatisticGateway):
    print()
    # Arrange

    # Category 1 with total time 0 (without intervals and time_all records)
    category_1 = await dl.category_loader.create(user_uuid=fx_user.uuid)
    category_1_time_total = 0

    # Category 2 open interval with closed intervals
    category_2 = await dl.category_loader.create(user_uuid=fx_user.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_2.uuid, started_at=2000)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_2.uuid, started_at=10, end_at=50)
    await dl.time_all_loader.create(user_uuid=fx_user.uuid, category_uuid=category_2.uuid, time_total=1000)
    category_2_time_total = 1040

    # Category 3 only closed intervals
    category_3 = await dl.category_loader.create(user_uuid=fx_user.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_3.uuid, started_at=10, end_at=30)
    await dl.time_all_loader.create(user_uuid=fx_user.uuid, category_uuid=category_3.uuid, time_total=200)
    category_3_time_total = 220

    arrange_categories_time_all = {
        category_1.uuid: category_1_time_total,
        category_2.uuid: category_2_time_total,
        category_3.uuid: category_3_time_total,
    }

    # Act
    res = await gateway_time_all.get_categories_statistic(user=fx_user)

    # Assert
    res_percent_sum = sum((time_percent.time_percent for time_percent in res.category_list), 0)
    res_category_uuid_set = {category.category_uuid for category in res.category_list}
    res_categories_time_all = {category.category_uuid: category.time_total for category in res.category_list}

    assert res_percent_sum == 100
    assert res_category_uuid_set == set(arrange_categories_time_all.keys())
    assert res_categories_time_all == arrange_categories_time_all
    assert res.user_uuid == fx_user.uuid
    assert sum([row.time_percent for row in res.category_list]) == 100.0


# pytest src/tests/ctx/statistic/test_statistic.py::test_get_category_statistic_category_not_found -v -s
async def test_get_category_statistic_category_not_found(
    dl: Dataloader, fx_user: UserEntity, gateway_time_all: StatisticGateway
):
    print()
    # Act
    with pytest.raises(EntityNotFound) as err:
        await gateway_time_all.get_categories_statistic(user=fx_user)
    # Assert
    assert f"{fx_user.uuid}" in str(err.value)


# pytest src/tests/ctx/statistic/test_statistic.py::test_get_category_statistic_categories_time_total_0 -v -s
async def test_get_category_statistic_categories_time_total_0(
    dl: Dataloader, fx_user: UserEntity, gateway_time_all: StatisticGateway
):
    print()
    # Arrange
    category_counter = 4
    _ = [await dl.category_loader.create(user_uuid=fx_user.uuid) for _ in range(category_counter)]
    # Act

    res = await gateway_time_all.get_categories_statistic(user=fx_user)

    # Assert
    assert res.user_uuid == fx_user.uuid
    assert sum([row.time_percent for row in res.category_list]) == 0.0
