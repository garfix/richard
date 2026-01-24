
from dataclasses import dataclass

from richard.entity.Relation import Relation
from richard.interface.SomeModel import SomeModel
from richard.interface.SomeSolver import SomeSolver
from richard.processor.semantic_composer.SemanticSentence import SemanticSentence


@dataclass(frozen=True)
class ExecutionContext:
    relation: Relation
    formal_parameters: list
    binding: dict
    solver: SomeSolver
    sentence: SemanticSentence
    model: SomeModel
