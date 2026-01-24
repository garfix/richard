from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.entity.ExecutionContext import ExecutionContext
from richard.module.optimizer.FrontResolveName import FrontResolveName
from richard.module.optimizer.IsolateIndependentParts import IsolateIndependentParts
from richard.module.optimizer.SortByCost import SortByCost


class OptimizerModule(SomeModule):

    def __init__(self) -> None:
        super().__init__()
        self.add_relation(Relation("optimize_frontize", query_function=self.optimize_frontize)),
        self.add_relation(Relation("optimize_isolate", query_function=self.optimize_isolate)),
        self.add_relation(Relation("optimize_cost_sort", query_function=self.optimize_cost_sort)),


    # ('optimize_frontize', SemIn, SemOut)
    # places `resolve_name` atoms up front
    def optimize_frontize(self, arguments: list, context: ExecutionContext) -> list[list]:
        sem_in = arguments[0]
        sem_out = FrontResolveName().sort(sem_in)
        return [
            [None, sem_out]
        ]


    # ('optimize_isolate', SemIn, SemOut)
    # performs David H.D. Warren's optimization
    def optimize_isolate(self, arguments: list, context: ExecutionContext) -> list[list]:
        sem_in = arguments[0]
        sem_out = IsolateIndependentParts().isolate(sem_in, context.sentence.root_variables)
        return [
            [None, sem_out]
        ]

    # ('optimize_cost_sort', SemIn, SemOut)
    # sorts atoms by decreasing cost
    def optimize_cost_sort(self, arguments: list, context: ExecutionContext) -> list[list]:
        sem_in = arguments[0]
        sem_out = SortByCost().sort(sem_in, context.solver, context.model)
        return [
            [None, sem_out]
        ]

