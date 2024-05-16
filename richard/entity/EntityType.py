from dataclasses import dataclass


@dataclass(frozen=True)
class EntityType:

    name: str
    get_all_ids: callable

