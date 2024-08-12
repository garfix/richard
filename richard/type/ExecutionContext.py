
from dataclasses import dataclass

from richard.interface.SomeSolver import SomeSolver


@dataclass(frozen=True)
class ExecutionContext:
    predicate: str
    binding: dict
    solver: SomeSolver
    