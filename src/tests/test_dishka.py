import uuid
from typing import Protocol
from dishka import provide, make_container, Provider, Scope

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
