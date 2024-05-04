from dataclasses import dataclass

from lib.entity.ParseTreeNode import ParseTreeNode
from lib.parser.entity.ChartState import ChartState


@dataclass
class WorkingStep:
    states: list[ChartState]
    nodes: list[ParseTreeNode]
    stateIndex: int


    def getCurrentState(self) -> ChartState:
        return self.states[self.stateIndex-1]


    def getCurrentNode(self) -> ParseTreeNode:
        return self.nodes[self.stateIndex-1]
