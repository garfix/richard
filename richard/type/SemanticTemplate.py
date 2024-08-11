from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticTemplate:
    args: list
    body: list[tuple]
