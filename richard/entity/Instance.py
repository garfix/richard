from dataclasses import dataclass


@dataclass(frozen=True)
class Instance:
    entity_name: str
    id: str
    