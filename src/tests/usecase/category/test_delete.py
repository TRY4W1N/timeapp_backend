import pytest
from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.category.delete import UsecaseCategoryDelete
from src.tests.dataloader import Dataloader


# pytest src/tests/usecase/category/test_delete.py::test_ok -v -s
async def test_ok(dl: Dataloader, fx_user: UserEntity, usecase_category_delete: UsecaseCategoryDelete):
    print()

    # Arrange
    # Created one category with 2 intervals
    uc = usecase_category_delete
    category_model = await dl.category_loader.create(user_uuid=fx_user.uuid)
    interval_fltr = {"user_uuid": fx_user.uuid, "category_uuid": category_model.uuid}

    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_model.uuid)
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_model.uuid)

    interval_before_model_list = await dl.interval_loader.get_lst(fltr=interval_fltr)
    interval_before_count = len(interval_before_model_list)
    assert interval_before_count == 2

    # Act
    result = await uc.execute(user=fx_user, category_uuid=CategoryId(category_model.uuid))

    # Assert
    with pytest.raises(Exception) as exc:
        category_model = await dl.category_loader.get(fltr=dict(uuid=category_model.uuid))
    assert "Not found" in str(exc.value)
    interval_after_model_list = await dl.interval_loader.get_lst(fltr=interval_fltr)
    interval_after_count = len(interval_after_model_list)

    assert result.category_uuid == category_model.uuid
    assert result.interval_count == 2
    assert interval_after_count == 0
