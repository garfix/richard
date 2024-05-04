from dataclasses import dataclass
from lib.type.PositionType import PositionType


@dataclass(frozen=True)
class RuleConstituent:
    predicate: str
    arguments: list[str]
    positionType: PositionType

    def equals(self, other):
        if self.predicate != other.predicate:
            return False
        
        if len(self.arguments) != len(other.arguments):
            return False
        
        if self.positionType != other.positionType:
            return False

        return True
    