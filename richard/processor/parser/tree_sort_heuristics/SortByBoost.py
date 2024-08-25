from richard.core.constants import CATEGORY_TOKEN
from richard.entity.ParseTreeNode import ParseTreeNode


class SortByBoost:
    """
    A bigger boost is better
    """
    def sort(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:

        results = []
        for tree in trees:
            score = self.get_boost(tree)
            results.append({'tree': tree, 'score': score})

        results.sort(key=lambda result: result['score'])

        return [result['tree'] for result in results]


    def get_boost(self, node: ParseTreeNode) -> int:
        return -node.rule.boost

