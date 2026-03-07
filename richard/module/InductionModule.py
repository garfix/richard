from richard.core.functions.terms import bind_variables, has_variables
from richard.core.functions.unification import unification
from richard.core.functions.variables import generate_variables
from richard.entity.InductionRule import InductionRule
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext
from richard.module.helper.SimpleInferenceRuleParser import SimpleInferenceRuleParser
from richard.module.induction.PlanAnalyzer import PlanAnalyzer
from richard.processor.semantic_composer.helper.VariableGenerator import VariableGenerator


class InductionModule(SomeModule):
    """
    This module, inspired by Robert Wilensky's PAM, analyzes the goals and plans of the actors in the story / dialog, and
    tries to predict their next moves
    """

    plan_analyzer: PlanAnalyzer
    fact_induction_rules: list[InductionRule]
    plan_analyzer_rules: list[InductionRule]
    deduction_rules: list[InductionRule]
    variable_generator: VariableGenerator


    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("induce_facts", query_function=self.induce_facts))
        self.add_relation(Relation("analyze_plans", query_function=self.analyze_plans))
        self.rules = {}
        self.variable_generator = VariableGenerator("ID")

        # the analyzer contains data that need to persist between sentences
        self.plan_analyzer = PlanAnalyzer()
        self.fact_induction_rules = []
        self.plan_analyzer_rules = []
        self.deduction_rules = []


    def import_fact_induction_rules(self, path: str):
        parser = SimpleInferenceRuleParser()
        with open(path) as rule_file:
            content = rule_file.read()
            rules, pos = parser.parse_induction_rules(content)
            if pos is not None:
                raise Exception("Unable to parse {} induction on token " + str(pos) + " in file " + path)
            for rule in rules:
                self.fact_induction_rules.append(rule)


    def import_plan_analyzer_rules(self, path: str):
        parser = SimpleInferenceRuleParser()
        with open(path) as rule_file:
            content = rule_file.read()
            rules, pos = parser.parse_induction_rules(content)
            if pos is not None:
                raise Exception("Unable to parse induction on token " + str(pos) + " in file " + path)
            for rule in rules:
                self.plan_analyzer_rules.append(rule)


    def import_deduction_rules(self, path: str):
        parser = SimpleInferenceRuleParser()
        with open(path) as rule_file:
            content = rule_file.read()
            rules, pos = parser.parse_rules(content)
            if pos is not None:
                raise Exception("Unable to parse induction on token " + str(pos) + " in file " + path)
            for rule in rules:
                self.deduction_rules.append(rule)


    # ('induce_facts', [body-atoms])
    def induce_facts(self, arguments: list, context: ExecutionContext) -> list[list]:
        atoms = arguments[0]

        if has_variables(atoms):
            raise Exception(f"Cannot induce facts based on unbound atoms. Please reify {atoms}")

        for rule in self.fact_induction_rules:
            variable_map = {}
            antecedent = generate_variables(rule.antecedent, self.variable_generator, variable_map)
            consequent = [generate_variables(atom, self.variable_generator, variable_map) for atom in rule.consequent]
            binding = unification(antecedent, atoms, {})
            if binding is not None:
                bound_consequent = bind_variables(consequent, binding)
                context.solver.write_atoms(bound_consequent)
        return [
            [None]
        ]


    # ('analyze_plans', [body-atoms])
    def analyze_plans(self, arguments: list, context: ExecutionContext) -> list[list]:
        atoms = arguments[0]

        if has_variables(atoms):
            raise Exception(f"Cannot induce facts based on unbound atoms. Please reify {atoms}")

        self.plan_analyzer.justify(atoms, self.plan_analyzer_rules, self.deduction_rules, context)

        return [
            [None]
        ]

