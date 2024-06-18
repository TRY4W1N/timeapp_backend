from dataclasses import asdict, dataclass

from src.domain.common.types.unset import UNSET


@dataclass
class UnsetDTO:

    def to_dict(self, exclude_unset: bool = True) -> dict:
        data = asdict(self)
        if exclude_unset:
            return {k: v for k, v in data.items() if v is not UNSET}
        return data
