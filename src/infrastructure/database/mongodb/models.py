from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Union


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
class CategoryTrackCurrentSubModel(Model):
    category_uuid: str
    interval_uuid: str
    started_at: int

    @classmethod
    def from_dict(cls, data: dict | None) -> Union["CategoryTrackCurrentSubModel", None]:
        if data is None:
            return None
        return CategoryTrackCurrentSubModel(
            category_uuid=data["category_uuid"],
            started_at=data["started_at"],
            interval_uuid=data["uuid"],
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


@dataclass
class TimeAllModel(Model):
    uuid: str
    user_uuid: str
    category_uuid: str
    total_time: int

    @classmethod
    def from_dict(cls, data: dict) -> "TimeAllModel":
        return TimeAllModel(
            uuid=data["uuid"],
            user_uuid=data["user_uuid"],
            category_uuid=data["category_uuid"],
            total_time=data["total_time"],
        )
