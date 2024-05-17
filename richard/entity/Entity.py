from dataclasses import dataclass


@dataclass(frozen=True)
class Entity:

    name: str
    get_all_ids: callable

