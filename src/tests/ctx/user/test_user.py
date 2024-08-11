from src.domain.ctx.user.dto import UserCreateDTO
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.const import get_default_categories
from src.tests.dataloader import Dataloader


# pytest src/tests/ctx/user/test_user.py::test_user_create_ok -v -s
async def test_user_create_ok(dl: Dataloader, gateway_user: UserGateway):
    print()
    # Arrange
    user_dto = UserCreateDTO(uuid=UserId("123"), name="Shrek", email="live_in_swapm@gmail.com")

    # Act
    res = await gateway_user.create(user=user_dto)

    # Assert result of user create
    assert res.uuid == user_dto.uuid
    assert res.email == user_dto.email
    assert res.name == user_dto.name

    # Assert of created default categories for user
    default_categories = get_default_categories()
    user_categories_list = await dl.category_loader.get_lst(fltr={"user_uuid": res.uuid})

    assert len(default_categories) == len(user_categories_list)
