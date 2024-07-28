from abc import abstractmethod

from richard.entity.ParseTreeNode import ParseTreeNode


class SomeParseTreeSortHeuristics:
    
    @abstractmethod
    def sort_trees(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:
        pass
