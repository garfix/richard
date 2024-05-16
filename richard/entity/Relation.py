from dataclasses import dataclass


@dataclass(frozen=True)
class Relation:

    name: str
    fields: list[str]
    get: callable
