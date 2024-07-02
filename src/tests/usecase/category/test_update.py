from datetime import datetime, timedelta

from src.domain.ctx.category.dto import CategoryUpdateDTO
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.category.update import UsecaseCategoryUpdate
from src.tests.dataloader import Dataloader, category_uuid_gen


# pytest src/tests/usecase/category/test_update.py::test_ok -v -s
async def test_ok(dl: Dataloader, fx_user: UserEntity, usecase_category_update: UsecaseCategoryUpdate):
    print()

    # Arrange
    category_uuid = CategoryId(category_uuid_gen())
    category_model = await dl.category_loader.create(
        uuid=category_uuid, user_uuid=fx_user.uuid, name="name", active=True
    )
    ## Two intervals for check correct result
    await dl.interval_loader.create(
        user_uuid=fx_user.uuid,
        category_uuid=category_uuid,
        started_at=int((datetime.now() - timedelta(hours=2)).timestamp()),
        end_at=int((datetime.now() - timedelta(hours=1)).timestamp()),
    )  # Ended
    interval_active_tracked = await dl.interval_loader.create(
        user_uuid=fx_user.uuid,
        category_uuid=category_uuid,
        started_at=int((datetime.now() - timedelta(hours=1)).timestamp()),
        end_at=None,
    )  # Active

    uc = usecase_category_update
    upd_name = "test_update_name"
    upd_active = False

    # Act
    updated_entity = await uc.execute(
        user=fx_user, category_uuid=category_uuid, obj=CategoryUpdateDTO(name=upd_name, active=upd_active)
    )

    # Assert
    assert updated_entity.uuid == category_uuid
    assert updated_entity.user_uuid == fx_user.uuid
    assert updated_entity.name == upd_name
    assert updated_entity.active == upd_active
    assert updated_entity.icon == category_model.icon
    assert updated_entity.icon_color == category_model.icon_color
    assert updated_entity.position == category_model.position
    assert updated_entity.track_current is not None
    assert updated_entity.track_current.category_uuid == category_uuid
    assert updated_entity.track_current.interval_uuid == interval_active_tracked.uuid
    assert updated_entity.track_current.started_at == interval_active_tracked.started_at
