from richard.constants import IGNORED, INFINITE
from richard.entity.Relation import Relation
from richard.entity.Variable import Variable
from richard.interface import SomeSolver
from richard.interface.SomeModule import SomeModule
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from richard.type.InferenceRule import InferenceRule


class InferenceModule(SomeModule):

    rules: dict[str, list[InferenceRule]]


    def __init__(self) -> None:
        self.relations = {}
        self.rules = {}

    
    def insert_rule(self, rule: InferenceRule):
        predicate = rule.head[0]
        self.relations[predicate] = Relation(self.handle_rule, IGNORED, [])
        if not predicate in self.rules:
            self.rules[predicate] = []
        self.rules[predicate].append(rule)


    def import_rules(self, path: str):
        parser = SimpleInferenceRuleParser()
        with open(path) as rule_file:
            for line in rule_file.readlines():
                if line.strip() == "":
                    continue
                rule = parser.parse(line)
                self.insert_rule(rule)


    def handle_rule(self, relation: str, values: list, solver: SomeSolver, binding: dict) -> list[list]:
        results = []
        for rule in self.rules[relation]:
            results.extend(self.solve_rule(rule, values, solver, binding))

        return results
    

    def solve_rule(self, rule: InferenceRule, values: list, solver: SomeSolver, binding: dict):
        rule_binding = {}

        rule_arguments = rule.head[1:]

        for rule_argument, value in zip(rule_arguments, values):
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
            
            for rule_argument, value in zip(rule_arguments, values):
                if isinstance(value, Variable):
                    if isinstance(rule_argument, Variable):
                        result.append(solution[rule_argument.name])    
                    else:
                        result.append(rule_argument)    
                else:
                    result.append(value)

            results.append(result)

        return results
