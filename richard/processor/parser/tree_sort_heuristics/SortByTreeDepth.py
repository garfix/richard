from richard.entity.ParseTreeNode import ParseTreeNode


class SortByTreeDepth:
    """
    Deeper trees are better
    """
    def sort(self, trees: list[ParseTreeNode]) -> list[ParseTreeNode]:

        results = []

        for tree in trees:
            score = self.get_depth(tree, 0)
            results.append({'tree': tree, 'score': score})

        results.sort(key=lambda result: result['score'])      

        return [result['tree'] for result in results]


    def get_depth(self, node: ParseTreeNode, base_depth: int) -> int:
        depth = base_depth - 1

        for child in node.children:
            depth = min(depth, self.get_depth(child, base_depth - 1))

        return depth
    
    