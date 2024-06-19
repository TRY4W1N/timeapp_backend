from dishka import AsyncContainer

from src.domain.ctx.auth.firebase.interface.gateway import IFirebaseApplicationGateway


# pytest src/tests/tmain/firebase/test_firebase_app.py::test_firebase_app -v -s
async def test_firebase_app(di: AsyncContainer):
    async with di() as container:
        app_1 = await container.get(IFirebaseApplicationGateway, component="AUTH")
        app_1.setup()
        app_1_id = id(app_1)

    async with di() as container:
        app_2 = await container.get(IFirebaseApplicationGateway, component="AUTH")
        assert app_2.is_setup is False
        app_2.setup()
        app_2_id = id(app_2)

    assert app_1_id != app_2_id
        
