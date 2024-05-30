from dataclasses import dataclass


@dataclass(frozen=True)
class Instance:
    entity: str
    id: str
    