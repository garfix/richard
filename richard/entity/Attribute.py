from dataclasses import dataclass


@dataclass(frozen=True)
class Attribute:

    name: str
    entities: list[str|None]


