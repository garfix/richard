from __future__ import annotations
from dataclasses import dataclass
from richard.type.PositionType import PositionType


@dataclass(frozen=True)
class RuleConstituent:
    predicate: str
    arguments: list[str]
    position_type: PositionType

    def equals(self, other: RuleConstituent):
        if self.predicate != other.predicate:
            return False
        
        if len(self.arguments) != len(other.arguments):
            return False
        
        if self.position_type != other.position_type:
            return False

        return True
    