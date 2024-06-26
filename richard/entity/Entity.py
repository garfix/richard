from dataclasses import dataclass


@dataclass(frozen=True)
class Entity:

    name: str
    attributes: list[str]
    modifiers: list[str]

