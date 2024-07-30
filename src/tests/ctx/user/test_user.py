from src.domain.ctx.user.dto import UserCreateDTO
from src.domain.ctx.user.interface.gateway import UserGateway
from src.domain.ctx.user.interface.types import UserId
from src.infrastructure.json_handler import read_default_categories_json
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
    default_categories = read_default_categories_json()
    user_default_categories_query = dl.category_loader._collection.aggregate([{"$match": {"user_uuid": res.uuid}}])
    user_default_categories_data = await user_default_categories_query.to_list(length=None)

    assert len(default_categories) == len(user_default_categories_data)
