from dataclasses import asdict, dataclass


@dataclass
class Model:

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class CategoryModel(Model):
    uuid: str
    user_uuid: str
    name: str
    icon: str
    icon_color: str
    position: int = 0
    disabled: bool = False
