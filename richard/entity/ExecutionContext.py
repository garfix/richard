
from dataclasses import dataclass

from richard.entity.Relation import Relation
from richard.interface.SomeSolver import SomeSolver


@dataclass(frozen=True)
class ExecutionContext:
    relation: Relation
    arguments: list
    binding: dict
    solver: SomeSolver
