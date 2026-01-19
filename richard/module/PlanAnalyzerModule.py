from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext


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
    def analyze_plans(self, values: list, context: ExecutionContext) -> list[list]:

        atoms = values[0]

        bindings = context.solver.solve([("recognize_plan", atoms)], context.binding)

        return [
            [None]
        ]

