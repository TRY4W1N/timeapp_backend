from src.domain.ctx.category.dto import CategoryFilterDTO
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.category.get_list import UsecaseCategoryGetList
from src.tests.dataloader import Dataloader


# pytest src/tests/usecase/category/test_list.py::test_ok -v -s
async def test_ok(dl: Dataloader, fx_user: UserEntity, usecase_category_get_list: UsecaseCategoryGetList):
    print()
    # Arrange
    name_fltr = "amogus"
    active_fltr = True

    # Category 1 ok
    category_model1 = await dl.category_loader.create(user_uuid=fx_user.uuid, active=True, name="amogusjjj", position=1)
    # Category 2 ok
    category_model2 = await dl.category_loader.create(
        user_uuid=fx_user.uuid, active=True, name="bobusAmogus", position=2
    )
    # Category 3 skip
    category_model3 = await dl.category_loader.create(user_uuid=fx_user.uuid, active=False, name="rnd", position=3)

    # Act
    fltr = CategoryFilterDTO(name__like=name_fltr, active__eq=active_fltr)
    category_list = await usecase_category_get_list.execute(user=fx_user, obj=fltr)

    # Assert
    assert len(category_list) == 2
    category_uuid_model_set = {category.uuid for category in [category_model1, category_model2]}
    category_uuid_set = {category.uuid for category in category_list}
    assert category_uuid_model_set == category_uuid_set
    assert category_model3.uuid not in category_uuid_set
    assert category_list[0].position < category_list[1].position
