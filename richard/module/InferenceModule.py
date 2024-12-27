from richard.core.atoms import bind_variables, get_atom_variables
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface import SomeSolver
from richard.interface.SomeModule import SomeModule
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from richard.type.ExecutionContext import ExecutionContext
from richard.type.InferenceRule import InferenceRule


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
            for line in rule_file.readlines():
                if line.strip() == "":
                    continue
                rule, pos = parser.parse(line)
                if rule is None:
                    raise Exception("Unable to parse inference: " + line + " on token " + str(pos))
                self.insert_rule(rule)


    def handle_rule(self, values: list, context: ExecutionContext) -> list[list]:
        results = []
        for rule in self.rules[context.relation.predicate]:
            results.extend(self.solve_rule(rule, context.arguments, context.solver, context.binding))

        return results


    def solve_rule(self, rule: InferenceRule, arguments: list, solver: SomeSolver, binding: dict):

        rule_arguments = rule.head[1:]
        # initialize with binding variables that do not affect this rule (but may be used later on)
        rule_binding = {key: value for (key, value) in binding.items() if key not in rule.get_all_variables()}

        for rule_argument, value in zip(rule_arguments, arguments):
            if isinstance(rule_argument, Variable):
                # bind variable
                if isinstance(value, Variable):
                    # A / E1
                    if value.name in binding:
                        rule_binding[rule_argument.name] = binding[value.name]
                else:
                    # A / 'john'
                    # check for conflicts
                    if rule_argument.name in rule_binding:
                        if rule_binding[rule_argument.name] != value:
                            return []
                    rule_binding[rule_argument.name] = value
            else:
                if isinstance(value, Variable):
                    # 'john' / E1
                    # check for conflicts
                    if value.name in binding:
                        if binding[value.name] != rule_argument:
                            return []
                else:
                    # 'john' / 'susan'
                    if value != rule_argument:
                        # value conflict in head
                        return []

        bindings = solver.solve(rule.body, rule_binding)

        results = []

        for solution in bindings:

            result = []

            for rule_argument, value in zip(rule_arguments, arguments):
                if isinstance(value, Variable):
                    if isinstance(rule_argument, Variable):
                        result.append(solution[rule_argument.name])
                    else:
                        result.append(rule_argument)
                else:
                    result.append(value)

            results.append(result)

        return results


    # ('learn_rule', head, [body-atoms])
    def learn_rule(self, values: list, context: ExecutionContext) -> list[list]:
        head, body = values

        if not isinstance(head, tuple):
            raise Exception("The head of a rule must be a single atom: " + str(head))

        bound_head = bind_variables(head, context.binding)
        bound_body = bind_variables(body, context.binding)

        self.insert_rule(InferenceRule(bound_head, bound_body))

        return [
            [None, None]
        ]

