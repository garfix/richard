from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Variable import Variable
from richard.interface.SomeParser import SomeParser
from richard.interface.SomeSemanticComposer import SomeSemanticComposer


class TupleComposer(SomeSemanticComposer):
    """
    Performs semantic composition on the product of the parser
    """
    
    parser: SomeParser


    def __init__(self, parser: SomeParser) -> None:
        super().__init__()
        self.parser = parser    

    
    def process(self, request: SentenceRequest) -> ProcessResult:

        number = 0

        def next_number():
            nonlocal number
            number += 1
            return number

        root = self.parser.get_tree(request)

        self.check_for_sem(root)
        
        semantics = self.compose_semantics(root, ["S"], next_number)
        return ProcessResult([semantics], "", [])    


    def check_for_sem(self, node: ParseTreeNode):
        if node.form == "" and node.rule.sem is None:
            raise Exception("Rule '" + node.rule.basic_form() + "' is missing key 'sem'")
        
        for child in node.children:
            self.check_for_sem(child)


    def compose_semantics(self, node: ParseTreeNode, incoming_variables: list[str], next_number: callable) -> list[tuple]:

        # map formal variables to unified, sentence-wide variables
        map = self.create_map(node, incoming_variables, next_number)

        # collect the semantics of the child nodes
        child_semantics = []
        for child, consequent in zip(node.children, node.rule.consequents):
            if not child.is_leaf_node():
                incoming_child_variables = [map[arg] for arg in consequent.arguments]
                semantic_function = self.compose_semantics(child, incoming_child_variables, next_number)               
                child_semantics.append(semantic_function)

        # create the semantics of this node by executing its function, passing the values of its children as arguments
        semantics = node.rule.sem(*child_semantics)

        # replace the formal parameters in the semantics with the unified variables
        unified_semantics = self.unify_variables(semantics, map)

        return unified_semantics
    
    
    def create_map(self, node: ParseTreeNode, incoming_variables: list[str], next_number: callable):
        # start variable map by mapping antecedent variables to incoming variables
        map = {}
        for i, arg in enumerate(node.rule.antecedent.arguments):
            map[arg] = incoming_variables[i]

        # complete map with other variables from the consequents
        for cons in node.rule.consequents:
            for i, arg in enumerate(cons.arguments):
                    if arg not in map:
                        map[arg] = "S" + str(next_number())
        return map
    

    def unify_variables(self, semantics: list[tuple], map: dict[str, str]) -> list[tuple]:
        unified_semantics = []
        for atom in semantics:
            new_atom = []
            for arg in atom:
                if isinstance(arg, Variable) and arg.name in map:
                    new_atom.append(Variable(map[arg.name]))
                else:
                    new_atom.append(arg)
            unified_semantics.append(tuple(new_atom))
        return unified_semantics


    def get_tuples(self, request: SentenceRequest) -> tuple:
        return request.get_current_product(self)
