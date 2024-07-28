from richard.constants import CATEGORY_TOKEN
from richard.entity.ParseTreeNode import ParseTreeNode


class SortByTokenCount:
    """
    Less nodes with the category 'token' is better
    """
    def sort(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:

        results = []

        for tree in trees:
            score = self.count_tokens(tree)
            results.append({'tree': tree, 'score': score})

        results.sort(key=lambda result: result['score'])

        return [result['tree'] for result in results]


    def count_tokens(self, node: ParseTreeNode) -> int:
        count = 1 if node.category == CATEGORY_TOKEN else 0

        for child in node.children:
            count += self.count_tokens(child)

        return count
    