from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class CooperModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:

        self.ds = data_source
        self.relations = {
            "resolve_name": Relation(query_function=self.resolve_name),
            "negate": Relation(query_function=self.negate),
        }


    def resolve_name(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0].lower()

        out_values = self.ds.select("name", ["name", "id"], [name, None])
        if len(out_values) > 0:
            return out_values
        else:
            id = context.arguments[1].name
            self.ds.insert("name", ["name", "id", ], [name, id])
            return [
                [name, id]
            ]


    # ('negate', atom)
    def negate(self, values: list, context: ExecutionContext) -> list[list]:
        atoms = values[0]

        results = context.solver.solve(atoms)

        # negated = list(atoms)
        # negated[0][0] = "not_" + negated[0][0]

        # results2 = context.solver.solve(negated)

        results2 = []

        if len(results) > 0:
            return [
                ['false']
            ]
        elif len(results2) > 0:
            return [
                ['true']
            ]
        else:
            return [
                ["unknown"]
            ]

    # # ('knows', [body-atoms])
    # def negate(self, values: list, context: ExecutionContext) -> list[list]:
    #     atoms = values[0]

    #     results = context.solver.solve([atoms])

    #     negated = atoms
    #     negated[0] = "not_" + negated[0]

    #     results2 = context.solver.solve([negated])

    #     if len(results) > 0:
    #         return [
    #             [False]
    #         ]
    #     elif len(results2) > 0:
    #         return [
    #             [True]
    #         ]
    #     else:
    #         return [
    #             ["UNKNOWN"]
    #         ]
