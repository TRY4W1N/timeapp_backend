from datetime import datetime, timedelta

import pytest

from src.domain.ctx.category.dto import (
    CategoryCreateDTO,
    CategoryFilterDTO,
    CategoryUpdateDTO,
)
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.interface.types import UserId
from src.tests.dataloader import Dataloader, category_uuid_gen, user_uuid_gen


# pytest src/tests/ctx/category/test_gateway.py::test_create -v -s
async def test_create(dl: Dataloader, gateway_category: CategoryGateway):
    print()
    # Arrange
    user_uuid = UserId(user_uuid_gen())
    name = "test_category"
    icon = "boba"
    icon_color = "rnd_color"
    postion = 1337

    # Act
    entity = await gateway_category.create(
        user_uuid=user_uuid, obj=CategoryCreateDTO(name=name, icon=icon, icon_color=icon_color, position=postion)
    )

    # Assert
    assert entity.uuid is not None
    assert entity.user_uuid == user_uuid
    assert entity.name == name
    assert entity.icon == icon
    assert entity.icon_color == icon_color
    assert entity.position == postion


# pytest src/tests/ctx/category/test_gateway.py::test_delete -v -s
async def test_delete(dl: Dataloader, gateway_category: CategoryGateway):
    print()
    # Arrange
    user_uuid = UserId(user_uuid_gen())
    category_uuid = CategoryId(category_uuid_gen())
    await dl.category_loader.create(uuid=category_uuid, user_uuid=user_uuid)
    await dl.interval_loader.create(user_uuid=user_uuid, category_uuid=category_uuid)
    await dl.interval_loader.create(user_uuid=user_uuid, category_uuid=category_uuid)

    # Act
    delete_result = await gateway_category.delete(user_uuid=user_uuid, category_uuid=category_uuid)

    # Assert
    with pytest.raises(Exception):
        await dl.category_loader.get(fltr=dict(uuid=category_uuid))
    interval_list = await dl.interval_loader.get_lst(fltr=dict(user_uuid=user_uuid, category_uuid=category_uuid))
    assert delete_result.category_uuid == category_uuid
    assert delete_result.user_uuid == user_uuid
    assert delete_result.interval_count == 2
    assert len(interval_list) == 0


# pytest src/tests/ctx/category/test_gateway.py::test_update -v -s
async def test_update(dl: Dataloader, gateway_category: CategoryGateway):
    print()
    # Arrange
    user_uuid = UserId(user_uuid_gen())
    category_uuid = CategoryId(category_uuid_gen())
    category_model = await dl.category_loader.create(uuid=category_uuid, user_uuid=user_uuid, name="name", active=True)

    # Two intervals for check correct result
    await dl.interval_loader.create(
        user_uuid=user_uuid,
        category_uuid=category_uuid,
        started_at=int((datetime.now() - timedelta(hours=2)).timestamp()),
        end_at=int((datetime.now() - timedelta(hours=1)).timestamp()),
    )  # Ended
    interval_active_tracked = await dl.interval_loader.create(
        user_uuid=user_uuid,
        category_uuid=category_uuid,
        started_at=int((datetime.now() - timedelta(hours=1)).timestamp()),
        end_at=None,
    )  # Active

    upd_name = "test_update_name"
    upd_active = False

    # Act
    updated_entity = await gateway_category.update(
        user_uuid=user_uuid, category_uuid=category_uuid, obj=CategoryUpdateDTO(name=upd_name, active=upd_active)
    )

    # Assert
    assert updated_entity.uuid == category_uuid
    assert updated_entity.user_uuid == user_uuid
    assert updated_entity.name == upd_name
    assert updated_entity.active == upd_active
    assert updated_entity.icon == category_model.icon
    assert updated_entity.icon_color == category_model.icon_color
    assert updated_entity.position == category_model.position
    assert updated_entity.track_current is not None
    assert updated_entity.track_current.category_uuid == category_uuid
    assert updated_entity.track_current.interval_uuid == interval_active_tracked.uuid
    assert updated_entity.track_current.started_at == interval_active_tracked.started_at


# pytest src/tests/ctx/category/test_gateway.py::test_lst_nested_interval_select -v -s
async def test_lst_nested_interval_select(dl: Dataloader, gateway_category: CategoryGateway):
    print()
    # Arrange
    user_uuid = UserId(user_uuid_gen())

    # Category 1 without interval
    category_uuid1 = CategoryId(f"1__{category_uuid_gen()}")
    category_model1 = await dl.category_loader.create(uuid=category_uuid1, user_uuid=user_uuid)

    # Category 2 with not active interval
    category_uuid2 = CategoryId(f"2__{category_uuid_gen()}")
    category_model2 = await dl.category_loader.create(uuid=category_uuid2, user_uuid=user_uuid)
    _ = await dl.interval_loader.create(
        user_uuid=user_uuid,
        category_uuid=category_uuid2,
        started_at=int(datetime.now().timestamp()),
        end_at=int((datetime.now() - timedelta(hours=1)).timestamp()),
    )

    # Category 3 with active and not active interval
    category_uuid3 = CategoryId(f"3__{category_uuid_gen()}")
    category_model3 = await dl.category_loader.create(uuid=category_uuid3, user_uuid=user_uuid)
    _ = await dl.interval_loader.create(
        user_uuid=user_uuid,
        category_uuid=category_uuid3,
        started_at=int(datetime.now().timestamp()),
        end_at=int((datetime.now() - timedelta(hours=1)).timestamp()),
    )
    interval_model3_active = await dl.interval_loader.create(
        user_uuid=user_uuid,
        category_uuid=category_uuid3,
        started_at=int(datetime.now().timestamp()),
        end_at=None,
    )

    # Act
    category_list = await gateway_category.lst(user_uuid=user_uuid, obj=CategoryFilterDTO())

    # Assert
    assert len(category_list) == 3
    category_dict = {category.uuid: category for category in category_list}

    ## Category 1 assert
    category_entity1 = category_dict.get(category_uuid1)
    assert category_entity1 is not None
    assert category_entity1.uuid == category_model1.uuid
    assert category_entity1.track_current is None

    ## Category 2 assert
    category_entity2 = category_dict.get(category_uuid2)
    assert category_entity2 is not None
    assert category_entity2.uuid == category_model2.uuid
    assert category_entity2.track_current is None

    ## Category 3 assert
    category_entity3 = category_dict.get(category_uuid3)
    assert category_entity3 is not None
    assert category_entity3.uuid == category_model3.uuid
    assert category_entity3.track_current is not None

    assert category_entity3.track_current.category_uuid == category_model3.uuid
    assert category_entity3.track_current.interval_uuid == interval_model3_active.uuid
    assert category_entity3.track_current.started_at == interval_model3_active.started_at


# pytest src/tests/ctx/category/test_gateway.py::test_lst_position_sort -v -s
async def test_lst_position_sort(dl: Dataloader, gateway_category: CategoryGateway):
    print()
    # Arrange
    user_uuid = UserId(user_uuid_gen())

    # Category 1 position 1
    category_model1 = await dl.category_loader.create(user_uuid=user_uuid, position=1)
    # Category 2 position 2
    category_model2 = await dl.category_loader.create(user_uuid=user_uuid, position=2)

    # Act
    category_list = await gateway_category.lst(user_uuid=user_uuid, obj=CategoryFilterDTO())

    # Assert
    assert category_list[0].uuid == category_model1.uuid
    assert category_list[1].uuid == category_model2.uuid
    assert category_list[0].position < category_list[1].position


# pytest src/tests/ctx/category/test_gateway.py::test_lst_fltr_name__like -v -s
async def test_lst_fltr_name__like(dl: Dataloader, gateway_category: CategoryGateway):
    print()
    # Arrange
    user_uuid = UserId(user_uuid_gen())
    name_fltr = "amogus"

    # Category 1 ok
    category_model1 = await dl.category_loader.create(user_uuid=user_uuid, name="amogusjjj")
    # Category 2 ok
    category_model2 = await dl.category_loader.create(user_uuid=user_uuid, name="bobusAmogus")
    # Category 3 skip
    category_model3 = await dl.category_loader.create(user_uuid=user_uuid, name="skipped")

    # Act
    category_list = await gateway_category.lst(user_uuid=user_uuid, obj=CategoryFilterDTO(name__like=name_fltr))

    # Assert
    assert len(category_list) == 2
    category_uuid_model_set = {category.uuid for category in [category_model1, category_model2]}
    category_uuid_set = {category.uuid for category in category_list}
    assert category_uuid_model_set == category_uuid_set
    assert category_model3.uuid not in category_uuid_set


# pytest src/tests/ctx/category/test_gateway.py::test_lst_fltr_active__eq -v -s
async def test_lst_fltr_active__eq(dl: Dataloader, gateway_category: CategoryGateway):
    print()
    # Arrange
    user_uuid = UserId(user_uuid_gen())
    active_fltr = True

    # Category 1 ok
    category_model1 = await dl.category_loader.create(user_uuid=user_uuid, active=True)
    # Category 2 ok
    category_model2 = await dl.category_loader.create(user_uuid=user_uuid, active=True)
    # Category 3 skip
    category_model3 = await dl.category_loader.create(user_uuid=user_uuid, active=False)

    # Act
    category_list = await gateway_category.lst(user_uuid=user_uuid, obj=CategoryFilterDTO(active__eq=active_fltr))

    # Assert
    assert len(category_list) == 2
    category_uuid_model_set = {category.uuid for category in [category_model1, category_model2]}
    category_uuid_set = {category.uuid for category in category_list}
    assert category_uuid_model_set == category_uuid_set
    assert category_model3.uuid not in category_uuid_set
