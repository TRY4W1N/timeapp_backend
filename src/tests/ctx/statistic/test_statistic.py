import pytest

from src.domain.common.exception.base import EntityNotFound
from src.domain.ctx.statistic.dto import StatisticFilterDTO
from src.domain.ctx.statistic.interface.gateway import StatisticGateway
from src.domain.ctx.user.entity import UserEntity
from src.tests.dataloader import Dataloader


async def _arrange_time_day_filter_time_to_unset(
    dl: Dataloader, user: UserEntity
) -> tuple[StatisticFilterDTO, dict[str, int]]:
    fake_time = 100
    fltr = StatisticFilterDTO(time_from=fake_time)

    category_1 = await dl.category_loader.create(user_uuid=user.uuid)
    category_2 = await dl.category_loader.create(user_uuid=user.uuid)

    # Time days and intervals in filter range
    await dl.time_day_loader.create(
        user_uuid=user.uuid, category_uuid=category_1.uuid, time_day=fake_time + 10, time_total=10
    )
    await dl.interval_loader.create(
        user_uuid=user.uuid, category_uuid=category_2.uuid, started_at=fake_time, end_at=fake_time + 100
    )

    arrange_categories_time_total = {
        category_1.uuid: 10,
        category_2.uuid: 100,
    }

    # Time days and intervals out of filter range
    category_3 = await dl.category_loader.create(user_uuid=user.uuid)
    await dl.time_day_loader.create(user_uuid=user.uuid, category_uuid=category_3.uuid, time_day=fake_time - 20)
    await dl.interval_loader.create(
        user_uuid=user.uuid, category_uuid=category_3.uuid, started_at=fake_time - 20, end_at=fake_time + 100
    )

    return fltr, arrange_categories_time_total


async def _arrange_time_day_filter_time_from_unset(
    dl: Dataloader, user: UserEntity
) -> tuple[StatisticFilterDTO, dict[str, int]]:
    fake_time = 100
    fltr = StatisticFilterDTO(time_to=fake_time)
    category_1 = await dl.category_loader.create(user_uuid=user.uuid)
    category_2 = await dl.category_loader.create(user_uuid=user.uuid)

    # Time days and intervals in filter range
    await dl.time_day_loader.create(
        user_uuid=user.uuid, category_uuid=category_1.uuid, time_day=fake_time - 10, time_total=20
    )
    await dl.interval_loader.create(
        user_uuid=user.uuid, category_uuid=category_2.uuid, started_at=fake_time - 50, end_at=fake_time
    )

    arrange_categories_time_total = {
        category_1.uuid: 20,
        category_2.uuid: 50,
    }

    # Time days and intervals out of filter range
    category_3 = await dl.category_loader.create(user_uuid=user.uuid)
    await dl.interval_loader.create(
        user_uuid=user.uuid, category_uuid=category_3.uuid, started_at=fake_time + 50, end_at=fake_time + 100
    )
    await dl.time_day_loader.create(
        user_uuid=user.uuid, category_uuid=category_3.uuid, time_day=fake_time + 20, time_total=10
    )

    return fltr, arrange_categories_time_total


async def _arrange_time_day_filter_time_from_set_time_to_set(
    dl: Dataloader, user: UserEntity
) -> tuple[StatisticFilterDTO, dict[str, int]]:
    fake_time = 100
    fltr = StatisticFilterDTO(time_to=fake_time + 100, time_from=fake_time - 100)

    category_1 = await dl.category_loader.create(user_uuid=user.uuid)
    category_2 = await dl.category_loader.create(user_uuid=user.uuid)

    # Time days and intervals in filter range
    await dl.time_day_loader.create(
        category_uuid=category_1.uuid, user_uuid=user.uuid, time_day=fake_time, time_total=10
    )
    await dl.interval_loader.create(
        user_uuid=user.uuid, category_uuid=category_2.uuid, started_at=fake_time, end_at=fake_time + 50
    )

    arrange_categories_time_total = {
        category_1.uuid: 10,
        category_2.uuid: 50,
    }

    # Time days and intervals out of filter range

    category_3 = await dl.category_loader.create(user_uuid=user.uuid)
    await dl.interval_loader.create(
        user_uuid=user.uuid, category_uuid=category_3.uuid, started_at=fake_time - 250, end_at=fake_time
    )
    await dl.interval_loader.create(
        user_uuid=user.uuid, category_uuid=category_3.uuid, started_at=fake_time + 250, end_at=fake_time + 300
    )
    await dl.time_day_loader.create(
        user_uuid=user.uuid, category_uuid=category_3.uuid, time_day=fake_time + 300, time_total=10
    )
    await dl.time_day_loader.create(
        user_uuid=user.uuid, category_uuid=category_3.uuid, time_day=fake_time - 300, time_total=10
    )

    return fltr, arrange_categories_time_total


async def _arrange_time_day_filter_time_from_unset_time_to_unset(
    dl: Dataloader, user: UserEntity
) -> tuple[StatisticFilterDTO, dict[str, int]]:
    fltr = StatisticFilterDTO()
    category_1 = await dl.category_loader.create(user_uuid=user.uuid)
    category_2 = await dl.category_loader.create(user_uuid=user.uuid)
    # Time days and intervals in filter range
    await dl.interval_loader.create(user_uuid=user.uuid, category_uuid=category_1.uuid, started_at=10, end_at=30)
    await dl.time_all_loader.create(user_uuid=user.uuid, category_uuid=category_2.uuid, time_total=40)

    arrange_categories_time_total = {
        category_1.uuid: 20,
        category_2.uuid: 40,
    }
    return fltr, arrange_categories_time_total


# pytest src/tests/ctx/statistic/test_statistic.py::test_get_category_statistic_filter_time_day_passed_ok -v -s
@pytest.mark.parametrize(
    "_arrange_fltr_data",
    [
        _arrange_time_day_filter_time_from_set_time_to_set,
        _arrange_time_day_filter_time_from_unset_time_to_unset,
        _arrange_time_day_filter_time_from_unset,
        _arrange_time_day_filter_time_to_unset,
    ],
)
async def test_get_category_statistic_filter_time_day_passed_ok(
    dl: Dataloader, fx_user: UserEntity, statistic_gateway: StatisticGateway, _arrange_fltr_data
):
    print()
    # Arrange
    fltr, arrange_categories_time_total_dict = await _arrange_fltr_data(dl=dl, user=fx_user)

    # Act
    res = await statistic_gateway.get_categories_statistic(user=fx_user, fltr=fltr)

    # Assert
    res_categories_total_time_dict = {category.category_uuid: category.time_total for category in res.category_list}

    assert res.user_uuid == fx_user.uuid
    if len(res.category_list) != 0:
        assert sum([row.time_percent for row in res.category_list]) == 100.0
    assert res_categories_total_time_dict == arrange_categories_time_total_dict


# pytest src/tests/ctx/statistic/test_statistic.py::test_get_category_statistic_without_filter_time_day_ok -v -s
async def test_get_category_statistic_without_filter_time_day_ok(
    dl: Dataloader, fx_user: UserEntity, statistic_gateway: StatisticGateway
):
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

    arrange_categories_time_dict = {
        category_1.uuid: category_1_time_total,
        category_2.uuid: category_2_time_total,
        category_3.uuid: category_3_time_total,
    }

    # Act
    res = await statistic_gateway.get_categories_statistic(user=fx_user, fltr=StatisticFilterDTO())

    # Assert
    res_categories_time_dict = {category.category_uuid: category.time_total for category in res.category_list}

    assert res_categories_time_dict == arrange_categories_time_dict
    assert res.user_uuid == fx_user.uuid
    assert sum([row.time_percent for row in res.category_list]) == 100.0


# pytest src/tests/ctx/statistic/test_statistic.py::test_get_category_statistic_category_not_found -v -s
async def test_get_category_statistic_category_not_found(
    dl: Dataloader, fx_user: UserEntity, statistic_gateway: StatisticGateway
):
    print()
    # Act
    res = await statistic_gateway.get_categories_statistic(user=fx_user, fltr=StatisticFilterDTO())
    assert res.user_uuid == fx_user.uuid
    # Assert
    assert isinstance(res.category_list, list)
    assert len(res.category_list) == 0


# pytest src/tests/ctx/statistic/test_statistic.py::test_get_category_statistic_categories_time_total_0 -v -s
async def test_get_category_statistic_categories_time_total_0(
    dl: Dataloader, fx_user: UserEntity, statistic_gateway: StatisticGateway
):
    print()
    # Arrange
    category_counter = 4
    _ = [await dl.category_loader.create(user_uuid=fx_user.uuid) for _ in range(category_counter)]
    # Act

    res = await statistic_gateway.get_categories_statistic(user=fx_user, fltr=StatisticFilterDTO())

    # Assert
    assert res.user_uuid == fx_user.uuid
    assert sum([row.time_percent for row in res.category_list]) == 0.0
