from dataclasses import dataclass


@dataclass(frozen=True)
class ReifiedVariable:
    name: str
    