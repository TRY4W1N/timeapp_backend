from datetime import datetime

from src.domain.ctx.category.interface.types import CategoryId
from src.domain.ctx.interval.interface.types import IntervalId
from src.domain.ctx.user.entity import UserEntity
from src.domain.usecases.interval.track_stop import UsecaseIntervalTrackStop
from src.tests.dataloader import Dataloader


# pytest src/tests/usecase/interval/test_stop.py::test_stop_interval_ok -v -s
async def test_stop_interval_ok(
    dl: Dataloader, fx_user: UserEntity, usecase_interval_track_stop: UsecaseIntervalTrackStop
):
    print()
    # Arrange
    uc = usecase_interval_track_stop
    category_model = await dl.category_loader.create()
    interval_model = await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_model.uuid)

    category_model_2 = await dl.category_loader.create()
    await dl.interval_loader.create(user_uuid=fx_user.uuid, category_uuid=category_model_2.uuid)

    started_at = datetime.now()
    timestamp = int(round(started_at.timestamp()))

    # Act
    res = await uc.execute(user=fx_user, category_uuid=CategoryId(category_model.uuid), stopped_at=timestamp)

    stopped_interval = await dl.interval_loader.get(
        fltr={"category_uuid": category_model.uuid, "user_uuid": fx_user.uuid}
    )

    # Assert
    assert res.category_uuid == CategoryId(category_model.uuid)
    assert res.interval_uuid == IntervalId(interval_model.uuid)
    assert res.user_uuid == fx_user.uuid

    assert isinstance(stopped_interval.end_at, int)
