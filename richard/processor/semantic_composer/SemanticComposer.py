from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Variable import Variable
from richard.interface.SomeParser import SomeParser
from richard.interface.SomeSemanticComposer import SomeSemanticComposer
from richard.entity.Composition import Composition


class SemanticComposer(SomeSemanticComposer):
    """
    Performs semantic composition on the product of the parser
    """
    
    parser: SomeParser


    def __init__(self, parser: SomeParser) -> None:
        super().__init__()
        self.parser = parser    

    
    def process(self, request: SentenceRequest) -> ProcessResult:

        number = 1

        def next_number():
            nonlocal number
            number += 1
            return number

        root = self.parser.get_tree(request)

        self.check_for_sem(root)
        
        semantics, inferences, intent = self.compose(root, ["S1"], next_number)
        composition = Composition(semantics, inferences, intent)
        return ProcessResult([composition], "", [])    


    def check_for_sem(self, node: ParseTreeNode):
        if node.form == "" and node.rule.sem is None:
            raise Exception("Rule '" + node.rule.basic_form() + "' is missing key 'sem'")
        
        for child in node.children:
            self.check_for_sem(child)


    def compose(self, node: ParseTreeNode, incoming_variables: list[str], next_number: callable) -> list[tuple]:

        # map formal variables to unified, sentence-wide variables
        map = self.create_map(node, incoming_variables, next_number)

        # collect the semantics of the child nodes
        child_semantics = []
        child_inferences = []
        child_intents = node.rule.intents
        for child, consequent in zip(node.children, node.rule.consequents):
            if not child.is_leaf_node():
                incoming_child_variables = [map[arg] for arg in consequent.arguments]
                child_semantic, child_inference, child_intent = self.compose(child, incoming_child_variables, next_number)               
                child_inferences.extend(child_inference)
                child_semantics.append(child_semantic)
                child_intents.extend(child_intent)
            elif child.rule.sem:
                child_semantics.append(child.rule.sem())
                child_inferences.extend(child.rule.inferences)
                child_intents.extend(child.rule.intents)

        # create the semantics of this node by executing its function, passing the values of its children as arguments
        child_semantic = node.rule.sem(*child_semantics)

        # replace the formal parameters in the semantics with the unified variables
        unified_semantics = self.unify_variables(child_semantic, map)

        # replace the formal parameters in the inferences with the unified variables
        unified_inferences = self.unify_variables(child_inferences, map)

        return unified_semantics, unified_inferences, child_intents
    
    
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
    

    def unify_variables(self, semantics: any, map: dict[str, str]) -> any:
        if isinstance(semantics, list):
            return [self.unify_variables(atom, map) for atom in semantics]
        elif isinstance(semantics, tuple):
            return tuple([self.unify_variables(term, map) for term in semantics])
        elif isinstance(semantics, Variable) and semantics.name in map:
            return Variable(map[semantics.name])
        else:
            return semantics


    def get_composition(self, request: SentenceRequest) -> Composition:
        return request.get_current_product(self)
    

    def format_tuples(self, request: SentenceRequest) -> str:
        return self.format_value(request.get_current_product(self).semantics)
    

    def format_value(self, value: any, indent: str = "\n") -> str:
        if isinstance(value, tuple):
            text = indent + "("
            sep = ""
            for element in value:
                text += sep + self.format_value(element, indent + "    ")
                sep = ", "
            text += ")"
        elif isinstance(value, list):
            if len(value) > 1:
                text = indent + "["
                for element in value:
                    text += self.format_value(element, indent + "    ")
                text += indent + "]"
            else:
                text = indent + "["
                for element in value:
                    text += self.format_value(element, "")
                text += "]"            
        elif isinstance(value, str):
            text = "'" + value + "'"
        else:
            text = str(value)
        return text
    