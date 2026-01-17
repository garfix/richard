from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticFunction:
    args: list
    body: list[tuple]
