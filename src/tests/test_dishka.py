import uuid
from typing import Protocol
from dishka import AsyncContainer, provide, make_container, Provider, Scope
from src.infrastructure.database.mongodb.database import DatabaseMongo


# Protocols
class Session(Protocol):

    @property
    def uuid(self) -> str: ...


class UserService(Protocol):
    uuid: str
    session: Session

    def do_something(self) -> str: ...


# Implements


class SessionMongo(Session):

    def __init__(self, uuid: str) -> None:
        self._uuid = uuid

    @property
    def uuid(self) -> str:
        return f"Mongo:{self._uuid}"


class UserServiceMongo(UserService):

    def __init__(self, uuid: str, session: Session) -> None:
        self.uuid = uuid
        self.session = session

    def do_something(self) -> str:
        return f"User(uuid={self.uuid}) on Session({self.session.uuid})"


# Provider


class ServiceProvider(Provider):

    def _rnd_uuid(self) -> str:
        print("Gen uuid!")
        return str(uuid.uuid4())

    @provide(scope=Scope.APP)
    def get_session(self) -> Session:
        print("Build session!")
        return SessionMongo(uuid=str(uuid.uuid4()))

    @provide(scope=Scope.REQUEST)
    def get_user_service(self, session: Session) -> UserService:
        print("Build UserService!")
        return UserServiceMongo(uuid=self._rnd_uuid(), session=session)


# pytest src/tests/test_dishka.py::test_simple -v -s
def test_simple():
    print()
    provider = ServiceProvider()
    container = make_container(provider)
    print("-" * 100)
    with container() as rc:
        service = rc.get(UserService)
        print(service.do_something())
        service = rc.get(UserService)
        print(service.do_something())
    print("-" * 100)
    with container() as rc:
        service = rc.get(UserService)
        print(service.do_something())
        service = rc.get(UserService)
        print(service.do_something())


# pytest src/tests/test_dishka.py::test_mongo_client -v -s
async def test_mongo_client(di: AsyncContainer):
    print()
    async with di() as container:
        print("*" * 77)
        database = await container.get(DatabaseMongo)
        user_collection, bobik_collection = database.get_collections("User", "Bobik")
        result = await user_collection.insert_one(dict(name="bobik", desc="dodik"))
        print(result)
        result = await bobik_collection.insert_one(dict(name="user", desc="aboba"))
        print(result)

        print("*" * 77)

        database = await container.get(DatabaseMongo)
        result = await user_collection.insert_one(dict(name="bobik", desc="dodik"))
        print(result)
        result = await bobik_collection.insert_one(dict(name="user", desc="aboba"))
        print(result)

    print("*" * 77)

    async with di() as container:
        database = await container.get(DatabaseMongo)
        user_collection, bobik_collection = database.get_collections("User", "Bobik")
        result = await user_collection.insert_one(dict(name="bobik", desc="dodik"))
        print(result)
        result = await bobik_collection.insert_one(dict(name="user", desc="aboba"))
        print(result)
