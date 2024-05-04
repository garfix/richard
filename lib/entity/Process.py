from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    id: str
