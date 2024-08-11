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
    color = "Test Icon Color"
    position = 0

    # Act
    result = await uc.execute(user=fx_user, obj=CategoryCreateDTO(name=name, icon=icon, color=color, position=position))

    # Assert
    assert result.uuid is not None
    assert result.name == name
    assert result.icon == icon
    assert result.color == color
    assert result.position == position

    assert result.track_current is None
