from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.SentenceRequest import SentenceRequest
from richard.interface.SomeParser import SomeParser
from richard.interface.SomeSemanticComposer import SomeSemanticComposer


class SemanticComposer(SomeSemanticComposer):
    """
    Performs semantic composition on the product of the parser
    """
    
    parser: SomeParser


    def __init__(self, parser: SomeParser) -> None:
        super().__init__()
        self.parser = parser    

    
    def process(self, request: SentenceRequest):
        parse_tree = self.parser.get_tree(request)
        semantic_function = self.compose_semantics(parse_tree)
        return [semantic_function]
    

    def compose_semantics(self, node: ParseTreeNode) -> callable:

        param_count = 0
        for child in node.children:
            if child.form == "":
                param_count += 1

        if (param_count == 0):
            return node.rule.sem()
        elif (param_count == 1):
            child1_sem = self.compose_semantics(node.children[0])
            return node.rule.sem(child1_sem)
        elif (param_count == 2):
            child1_sem = self.compose_semantics(node.children[0])
            child2_sem = self.compose_semantics(node.children[1])
            return node.rule.sem(child1_sem, child2_sem)
        elif (param_count == 3):
            child1_sem = self.compose_semantics(node.children[0])
            child2_sem = self.compose_semantics(node.children[1])
            child3_sem = self.compose_semantics(node.children[2])
            return node.rule.sem(child1_sem, child2_sem, child3_sem)
        else:
            raise Exception("Parameter count of " + param_count + " not yet implemented")
    

    def get_semantic_function(self, request: SentenceRequest) -> callable:
        return request.get_current_product(self)
