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
        self.relations = {
             "learn_rule": Relation(query_function=self.learn_rule),
        }
        self.rules = {}


    def insert_rule(self, rule: InferenceRule):
        predicate = rule.head[0]
        self.relations[predicate] = Relation(query_function=self.handle_rule)
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
        for rule in self.rules[context.predicate]:
            results.extend(self.solve_rule(rule, context.arguments, context.solver, context.binding))

        return results


    def solve_rule(self, rule: InferenceRule, arguments: list, solver: SomeSolver, binding: dict):

        rule_arguments = rule.head[1:]
        rule_binding = binding.copy()

        for rule_argument, value in zip(rule_arguments, arguments):
            if isinstance(rule_argument, Variable):
                # bind variable
                if isinstance(value, Variable):
                    # A / E1
                    if value.name in binding:
                        rule_binding[rule_argument.name] = binding[value.name]
                else:
                    # A / 'john'
                    rule_binding[rule_argument.name] = value
            else:
                # check for conflicts
                if isinstance(value, Variable):
                    # 'john' / E1
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

        bound_head = bind_variables(head, context.binding)
        bound_body = bind_variables(body, context.binding)

        self.insert_rule(InferenceRule(bound_head, bound_body))

        return [
            [None, None]
        ]

