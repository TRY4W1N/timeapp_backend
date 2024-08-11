from datetime import datetime

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.interval.track_start import UsecaseIntervalTrackStart
from src.tests.dataloader import Dataloader


# pytest src/tests/usecase/interval/test_start.py::test_start_interval_ok -v -s
async def test_start_interval_ok(
    dl: Dataloader, fx_user: UserEntity, usecase_interval_track_start: UsecaseIntervalTrackStart
):
    print()
    # Arrange
    uc = usecase_interval_track_start
    category_model = await dl.category_loader.create(user_uuid=fx_user.uuid)

    category_model_2 = await dl.category_loader.create()
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_model_2.uuid)

    started_at = datetime.now()
    timestamp = int(round(started_at.timestamp()))

    # Act
    res = await uc.execute(user=fx_user, category_uuid=CategoryId(category_model.uuid))

    # Assert
    assert res.user_uuid == fx_user.uuid
    assert res.category_uuid == CategoryId(category_model.uuid)
    assert isinstance(res.interval_uuid, str)
