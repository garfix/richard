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

        # start variable map
        map = {}
        for i, arg in enumerate(node.rule.antecedent.arguments):
            map[arg] = incoming_variables[i]

        # complete map with other variables
        for cons in node.rule.consequents:
            for i, arg in enumerate(cons.arguments):
                    if arg not in map:
                        map[arg] = "S" + str(next_number())

        print(node.category)
        print(map)

        # collect the semantics of the child nodes
        child_semantics = []
        for i, child in enumerate(node.children):
            if child.form == "":
                incoming_child_variables = [map[arg] for arg in node.rule.consequents[i].arguments]
                print(child.category, incoming_child_variables)
                semantic_function = self.compose_semantics(child, incoming_child_variables, next_number)               
                child_semantics.append(semantic_function)

        # create the semantics of this node by executing its (outer) semantic function, passing the 
        # functions of its children as arguments
        #
        # if you're porting this construct to a language that doesn't support list expansion, 
        # create a switch with a case for each number of arguments (up to 10 or so)
        semantics = node.rule.sem(*child_semantics)

        print(semantics)

        # replace variables in semantics
        unified_semantics = []
        for atom in semantics:
            new_atom = []
            for arg in atom:
                if isinstance(arg, Variable) and arg.name in map:
                    new_atom.append(Variable(map[arg.name]))
                else:
                    new_atom.append(arg)
            unified_semantics.append(tuple(new_atom))

        print(unified_semantics)
        print()

        return unified_semantics


    def get_tuples(self, request: SentenceRequest) -> tuple:
        return request.get_current_product(self)
