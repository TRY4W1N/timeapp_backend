from time import sleep
from src.domain.ctx.category.dto import CategoryCreateDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.category.create import UsecaseCategoryCreate
from src.tests.dataloader import Dataloader


# pytest src/tests/usecase/category/test_create.py::test_ok -v -s
async def test_ok(dl: Dataloader, fx_user: UserEntity, usecase_category_create: UsecaseCategoryCreate):
    print()

    # Arrange
    uc = usecase_category_create
    name = "Test Category"
    icon = "Test Icon"
    icon_color = "Test Icon Color"
    position = 0

    # Act
    result = await uc.execute(
        user=fx_user, obj=CategoryCreateDTO(name=name, icon=icon, icon_color=icon_color, position=position)
    )

    # Assert
    assert result.uuid is not None
    assert result.name == name
    assert result.icon == icon
    assert result.icon_color == icon_color
    assert result.position == position

    assert result.track_info.category_uuid  == result.uuid
    assert result.track_info.interval_uuid is None
    assert result.track_info.active is False
    assert result.track_info.started_at is None

