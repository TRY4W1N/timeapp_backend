import pytest

from src.domain.ctx.user.entity import UserEntity
from src.tests.dataloader import Dataloader


@pytest.fixture(scope="function")
async def fx_user(dl: Dataloader) -> UserEntity:
    user_model = await dl.user_loader.create()
    return UserEntity(uuid=user_model.uuid, email=user_model.email, name=user_model.name)
