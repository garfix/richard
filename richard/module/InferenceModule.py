from richard.core.functions.atoms import bind_variables, create_argument_binding
from richard.core.functions.results import bindings_to_tuple_results
from richard.entity.Relation import Relation
from richard.interface import SomeSolver
from richard.interface.SomeModule import SomeModule
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from richard.entity.ExecutionContext import ExecutionContext
from richard.entity.InferenceRule import InferenceRule


class InferenceModule(SomeModule):
    """
    This module handles very basic Prolog-like facts and inferences.
    """

    rules: dict[str, list[InferenceRule]]


    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("learn_rule", query_function=self.learn_rule))
        self.rules = {}


    def insert_rule(self, rule: InferenceRule):
        predicate = rule.head[0]
        self.add_relation(Relation(predicate, query_function=self.handle_rule))
        if not predicate in self.rules:
            self.rules[predicate] = []
        self.rules[predicate].append(rule)


    def import_rules(self, path: str):
        parser = SimpleInferenceRuleParser()
        with open(path) as rule_file:
            content = rule_file.read()
            rules, pos = parser.parse_rules(content)
            if pos is not None:
                raise Exception("Unable to parse inference on token " + str(pos) + " in file " + path)
            for rule in rules:
                self.insert_rule(rule)


    def handle_rule(self, arguments: list, context: ExecutionContext) -> list[list]:
        results = []
        for rule in self.rules[context.relation.predicate]:
            results.extend(self.solve_rule(rule, arguments, context.solver, context.binding))

        return results


    def solve_rule(self, rule: InferenceRule, arguments: list, solver: SomeSolver, binding: dict):

        formal_parameters = rule.head[1:]

        rule_binding = create_argument_binding(formal_parameters, arguments, binding)
        if rule_binding is None:
            return []

        if len(rule.body) == 0:
            bindings = [ rule_binding ]
        else:
            bindings = solver.solve(rule.body, rule_binding)

        results = bindings_to_tuple_results(formal_parameters, arguments, bindings)

        return results


    # ('learn_rule', head, [body-atoms])
    def learn_rule(self, arguments: list, context: ExecutionContext) -> list[list]:
        head, body = arguments

        if not isinstance(head, tuple):
            raise Exception("The head of a rule must be a single atom: " + str(head))

        bound_head = bind_variables(head, context.binding)
        bound_body = bind_variables(body, context.binding)

        self.insert_rule(InferenceRule(bound_head, bound_body))

        return [
            [None, None]
        ]

