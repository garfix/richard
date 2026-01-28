from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext
# from richard.module.plan_analyzer.PlanAnalyzer import PlanAnalyzer


class PlanAnalyzerModule(SomeModule):
    """
    This module, inspired by Robert Wilensky's PAM, analyzes the goals and plans of the actors in the story / dialog, and
    tries to predict their next moves
    """
    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("analyze_plans", query_function=self.analyze_plans))
        self.rules = {}


    # ('analyze_plans', [body-atoms])
    def analyze_plans(self, arguments: list, context: ExecutionContext) -> list[list]:

        atoms = arguments[0]

        # induce likely facts from the input
        # inductions = induce()
        inductions = atoms

        init_rules = []
        sub_for = []
        plans_for = []
        instof = []
        inference_rules = []

        # plan_analyzer = PlanAnalyzer(init_rules, sub_for, plans_for, instof, inference_rules)
        # plan_analyzer.justify(inductions)

        # bindings = context.solver.solve([("recognize_plan", atoms)], context.binding)

        return [
            [None]
        ]

