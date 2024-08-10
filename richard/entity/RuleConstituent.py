from __future__ import annotations
from dataclasses import dataclass
from richard.type.PositionType import PositionType


class RuleConstituent:
    predicate: str
    arguments: list[str]
    position_type: PositionType
    hash: int


    def __init__(self, predicate: str, arguments: list[str], position_type: PositionType):
        self.predicate = predicate
        self.arguments = arguments
        self.position_type = position_type

        h = [c for c in arguments] + [self.predicate, self.position_type]
        self.hash = hash(tuple(h))
  

    def equals(self, other: RuleConstituent):
        if self.predicate != other.predicate:
            return False
        
        if len(self.arguments) != len(other.arguments):
            return False
      
        if self.position_type != other.position_type:
            return False

        return True
    

    def __str__(self) -> str:
        return self.predicate + "(" + ", ".join([argument for argument in self.arguments]) + ")"
    