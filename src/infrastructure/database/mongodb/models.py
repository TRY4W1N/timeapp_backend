from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass


@dataclass
class Model(ABC):

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict) -> "Model": ...


@dataclass
class UserModel(Model):
    uuid: str
    name: str
    email: str

    @classmethod
    def from_dict(cls, data: dict) -> "UserModel":
        return UserModel(uuid=data["uuid"], name=data["name"], email=data["email"])


@dataclass
class CategoryTrackInfoSubModel(Model):
    category_uuid: str
    active: bool
    started_at: int | None
    interval_uuid: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "CategoryTrackInfoSubModel":
        return CategoryTrackInfoSubModel(
            category_uuid=data["category_uuid"],
            active=data["active"],
            started_at=data["started_at"],
            interval_uuid=data["interval_uuid"],
        )


@dataclass
class CategoryModel(Model):
    uuid: str
    user_uuid: str
    name: str
    icon: str
    icon_color: str
    position: int = 0
    active: bool = True

    @classmethod
    def from_dict(cls, data: dict) -> "CategoryModel":
        return CategoryModel(
            uuid=data["uuid"],
            user_uuid=data["user_uuid"],
            name=data["name"],
            active=data["active"],
            icon=data["icon"],
            icon_color=data["icon_color"],
            position=data["position"],
        )

@dataclass
class IntervalModel(Model):
    uuid: str
    user_uuid: str
    category_uuid: str
    started_at: int
    end_at: int | None
    
    @classmethod
    def from_dict(cls, data: dict) -> "IntervalModel":
        return IntervalModel(
            uuid=data["uuid"],
            user_uuid=data["user_uuid"],
            category_uuid=data["category_uuid"],
            started_at=data["started_at"],
            end_at=data["end_at"],
        )