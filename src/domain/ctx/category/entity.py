from dataclasses import dataclass


@dataclass
class CategoryEntity:
    uuid: str
    user_uuid: str
    name: str
    disabled: bool
    icon: str
    icon_color: str
    position: int
    on_track: bool
