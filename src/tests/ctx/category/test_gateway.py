from datetime import datetime, timedelta

import pytest

from src.domain.ctx.category.dto import CategoryCreateDTO, CategoryUpdateDTO
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
