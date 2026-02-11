from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext
from richard.module.induction.PlanAnalyzer import PlanAnalyzer


class PlanAnalyzerModule(SomeModule):
    """
    This module, inspired by Robert Wilensky's PAM, analyzes the goals and plans of the actors in the story / dialog, and
    tries to predict their next moves
    """

    plan_analyzer: PlanAnalyzer


    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("induce_facts", query_function=self.induce_facts))
        self.add_relation(Relation("analyze_plans", query_function=self.analyze_plans))
        self.rules = {}

        # the analyzer contains data that need to persist between sentences
        self.plan_analyzer = PlanAnalyzer()


    def import_fact_induction_rules(self, path: str):
        pass


    def import_plan_analyzer_rules(self, path: str):
        pass


    # ('induce_facts', [body-atoms])
    def induce_facts(self, arguments: list, context: ExecutionContext) -> list[list]:
        return []


    # ('analyze_plans', [body-atoms])
    def analyze_plans(self, arguments: list, context: ExecutionContext) -> list[list]:

        print('X')

        atoms = arguments[0]

        # induce likely facts from the input
        # inductions = induce()
        inductions = atoms

        init_rules = []
        sub_for = []
        plans_for = []
        instof = []
        inference_rules = []

        self.plan_analyzer.justify(inductions, context)

        # bindings = context.solver.solve([("recognize_plan", atoms)], context.binding)

        return [
            [None]
        ]

