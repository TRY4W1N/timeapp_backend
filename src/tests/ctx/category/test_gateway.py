from src.domain.ctx.category.dto import CategoryCreateDTO
from src.domain.ctx.category.interface.gateway import CategoryGateway
from src.domain.ctx.user.interface.types import UserId
from src.tests.dataloader import Dataloader, user_uuid_gen


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
