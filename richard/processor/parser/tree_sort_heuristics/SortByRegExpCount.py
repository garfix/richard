from richard.core.constants import POS_TYPE_REG_EXP
from richard.entity.ParseTreeNode import ParseTreeNode


class SortByRegExpCount:
    """
    Less nodes based on a regular expression is better
    """
    def sort(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:

        results = []
        for tree in trees:
            score = self.count_tokens(tree)
            results.append({'tree': tree, 'score': score})

        results.sort(key=lambda result: result['score'])

        return [result['tree'] for result in results]


    def count_tokens(self, node: ParseTreeNode) -> int:
        count = 0
        if node.rule.antecedent.position_type == POS_TYPE_REG_EXP:
            count = 1

        for child in node.children:
            count += self.count_tokens(child)

        return count
