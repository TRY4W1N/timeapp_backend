from src.domain.ctx.category.dto import CategoryAddDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.category.add import UsecaseCategoryAdd
from src.tests.dataloader import Dataloader


# pytest src/tests/usecase/category/test_add.py::test_add -v -s
async def test_add(dl: Dataloader, fx_user: UserEntity, usecase_category_add: UsecaseCategoryAdd):
    print()

    # Arrange
    uc = usecase_category_add
    name = "Test Category"
    icon = "Test Icon"
    icon_color = "Test Icon Color"
    position = 0

    # Act
    result = await uc.execute(
        user=fx_user, obj=CategoryAddDTO(name=name, icon=icon, icon_color=icon_color, position=position)
    )

    # Assert
    assert result.uuid is not None
    assert result.name == name
    assert result.icon == icon
    assert result.icon_color == icon_color
    assert result.position == position
    assert result.on_track is False
