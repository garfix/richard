from richard.entity.ReifiedVariable import ReifiedVariable
from richard.entity.ParseTreeNode import ParseTreeNode
from richard.entity.ProcessResult import ProcessResult
from richard.entity.SentenceRequest import SentenceRequest
from richard.entity.Variable import Variable
from richard.interface.SomeClearableDb import SomeClearableDb
from richard.interface.SomeProcessor import SomeProcessor
from richard.interface.SomeQueryOptimizer import SomeQueryOptimizer
from richard.processor.parser.BasicParserProduct import BasicParserProduct
from richard.processor.semantic_composer.SemanticComposerProduct import SemanticComposerProduct
from richard.processor.semantic_composer.helper.VariableGenerator import VariableGenerator
from richard.type.SemanticTemplate import SemanticTemplate


class SemanticComposer(SomeProcessor):
    """
    Performs semantic composition on the product of the parser
    Opimizes the composition for speed of execution
    """

    parser: SomeProcessor
    query_optimizer: SomeQueryOptimizer
    variable_generator: VariableGenerator
    sentence_context: SomeClearableDb


    def __init__(self, parser: SomeProcessor) -> None:
        super().__init__()
        self.parser = parser
        self.query_optimizer = None
        self.variable_generator = VariableGenerator("$")
        self.sentence_context = None


    def get_name(self) -> str:
        return "Composer"


    def process(self, request: SentenceRequest) -> ProcessResult:

        if self.sentence_context:
            self.sentence_context.clear()

        incoming: BasicParserProduct = request.get_current_product(self.parser)
        parse_tree = incoming.parse_tree

        self.check_for_sem(parse_tree)

        root_variables = [self.variable_generator.next() for _ in parse_tree.rule.antecedent.arguments]
        semantics, inferences = self.compose(parse_tree, root_variables)

        if self.query_optimizer:
            semantics_iterations = self.query_optimizer.optimize(semantics, root_variables)
        else:
            semantics_iterations = {"Semantics": semantics}

        product = SemanticComposerProduct(semantics_iterations, inferences, root_variables)
        return ProcessResult([product], "")


    def check_for_sem(self, node: ParseTreeNode):
        if node.form == "" and node.rule.sem is None:
            raise Exception("Rule '" + str(node.rule) + "' is missing key 'sem'")

        for child in node.children:
            self.check_for_sem(child)


    def compose(self, node: ParseTreeNode, incoming_variables: list[str]) -> list[tuple]:

        # map formal variables to unified, sentence-wide variables
        map = self.create_map(node, incoming_variables)

        # collect the semantics of the child nodes
        child_semantics = []
        inferences = []

        inferences.extend(node.rule.inferences)

        for child, consequent in zip(node.children, node.rule.consequents):
            if not child.is_leaf_node():
                incoming_child_variables = [map[arg] for arg in consequent.arguments]
                semantics, child_inference = self.compose(child, incoming_child_variables)
                inferences.extend(child_inference)
                child_semantics.append(semantics)
            elif child.rule.sem:
                child_semantics.append(child.rule.sem())

        # create the semantics of this node by executing its function, passing the values of its children as arguments
        semantics = node.rule.sem(*child_semantics)

        # extend the map with variables found in the result of the semantics function
        self.extend_map_with_semantics(map, semantics)

        # replace the formal parameters in the semantics with the unified variables
        unified_semantics = self.unify_variables(semantics, map)

        # replace the formal parameters in the inferences with the unified variables
        unified_inferences = self.unify_variables(inferences, map)

        return unified_semantics, unified_inferences


    def create_map(self, node: ParseTreeNode, incoming_variables: list[str]):
        # start variable map by mapping antecedent variables to incoming variables
        map = {}
        for i, arg in enumerate(node.rule.antecedent.arguments):
            map[arg] = incoming_variables[i]

        # complete map with other variables from the consequents
        for cons in node.rule.consequents:
            for i, arg in enumerate(cons.arguments):
                    if arg not in map:
                        map[arg] = self.variable_generator.next()

        return map


    def extend_map_with_semantics(self, map: dict, semantics: list[tuple]):
        # only lists of atoms for now
        if isinstance(semantics, list):
            for atom in semantics:
                for arg in atom:
                    # since we're late in the game, don't replace variables that have already been replaced
                    if isinstance(arg, Variable) and arg.name not in map and not self.variable_generator.isinstance(arg):
                        map[arg.name] = self.variable_generator.next()


    def unify_variables(self, semantics: any, map: dict[str, str]) -> any:
        if isinstance(semantics, list):
            return [self.unify_variables(atom, map) for atom in semantics]
        elif isinstance(semantics, tuple):
            return tuple([self.unify_variables(term, map) for term in semantics])
        elif isinstance(semantics, SemanticTemplate):
            return SemanticTemplate(semantics.args, self.unify_variables(semantics.body, map))
        elif isinstance(semantics, Variable) and semantics.name in map:
            return Variable(map[semantics.name])
        elif isinstance(semantics, ReifiedVariable) and semantics.name in map:
            return map[semantics.name]
        else:
            return semantics

