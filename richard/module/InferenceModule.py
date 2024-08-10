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
        self.relations[predicate] = Relation(self.handle_rule, IGNORED, [INFINITE, INFINITE])
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
        for argument, term in zip(rule_arguments, values):
            if isinstance(argument, Variable):
                if not isinstance(term, Variable):
                    rule_binding[argument.name] = term

        solutions = solver.solve(rule.body, rule_binding)

        results = []
        for solution in solutions:
            # extend the incoming binding
            result = binding.copy()
            # check needed for a variable that occurs twice
            conflict = False

            # go through all arguments
            for i, term in enumerate(values):
                # variable?
                if isinstance(term, Variable):
                    # if the variable was bound already, no need to assign it
                    # also no need to check for conflict, because the type may be different and that's ok
                    if term.name not in binding:
                        # check for conflict with previous same variable
                        if term.name in result and result[term.name] != solution[i]:
                            conflict = True
                        # extend the binding
                        result[term.name] = solution[i]

            if conflict:
                continue

            results.append(result)

        return results
    
