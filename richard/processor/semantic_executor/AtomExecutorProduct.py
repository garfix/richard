from dataclasses import dataclass


@dataclass
class AtomExecutorProduct:
    bindings: list[dict]
    stats: dict[str, int]

