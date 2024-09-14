from richard.entity.ParseTreeNode import ParseTreeNode
from richard.processor.parser.tree_sort_heuristics.SortByBoost import SortByBoost
from richard.processor.parser.tree_sort_heuristics.SortByTokenCount import SortByTokenCount
from richard.processor.parser.tree_sort_heuristics.SortByTreeDepth import SortByTreeDepth


class BasicParseTreeSortHeuristics:
    def sort_trees(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:
        # in order of increasing priority:
        trees = SortByTreeDepth().sort(trees)
        trees = SortByTokenCount().sort(trees)
        trees = SortByBoost().sort(trees)
        return trees
