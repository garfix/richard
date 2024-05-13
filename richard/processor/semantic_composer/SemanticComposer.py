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
        # collect the semantic functions of the child nodes
        child_semantics = []
        for child in node.children:
            if child.form == "":
                child_semantics.append(self.compose_semantics(child))

        # create the semantics of this node by executing its (outer) semantic function, passing the 
        # functions of its children as arguments
        #
        # if you're porting this construct to a language that doesn't support list expansion, 
        # create a switch with a case for each number of arguments (up to 10 or so)
        return node.rule.sem(*child_semantics)
    

    def get_semantic_function(self, request: SentenceRequest) -> callable:
        return request.get_current_product(self)
