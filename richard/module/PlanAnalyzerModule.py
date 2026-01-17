from richard.data_source.Sqlite3DataSource import Sqlite3DataSource
from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext


class PlanAnalyzerModule(SomeModule):
    """
    This module, inspired by Robert Wilensky's PAM, analyzes the goals and plans of the actors in the story / dialog, and
    tries to predict their next moves
    """
    data_source: SomeDataSource

    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.add_relation(Relation("analyze_plans", query_function=self.analyze_plans))
        self.add_relation(Relation("goal", query_function=self.goal))
        self.data_source = data_source
        self.rules = {}


    # ('goal', [body-atoms])
    def goal(self, values: list, context: ExecutionContext) -> list[list]:
        pass


    # ('analyze_plans', [body-atoms])
    def analyze_plans(self, values: list, context: ExecutionContext) -> list[list]:

        atoms = values[0]

        bindings = context.solver.solve([("recognize_plan", atoms)], context.binding)

        return [
        ]

