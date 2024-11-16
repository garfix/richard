from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class SIRModule(SomeModule):

    ds: SomeDataSource


    def __init__(self, data_source: SomeDataSource) -> None:
        super().__init__()
        self.ds = data_source
        self.add_relation(Relation("add_relation", query_function=self.create_relation)),


    def common_query(self, values: list, context: ExecutionContext) -> list[list]:
        results = self.ds.select(context.relation.predicate, context.relation.arguments, values)
        if len(results) > 0:
            return results
        else:
            return [
                values[:-1] + ["unknown"]
            ]


    def common_write(self, values: list, context: ExecutionContext) -> list[list]:
        # print(context.predicate, values)
        self.ds.insert(context.relation.predicate, context.relation.arguments, values)


    # ('create_relation', predicate, arguments)
    def create_relation(self, values: list, context: ExecutionContext) -> list[list]:

        predicate, arguments = values

        self.add_relation(Relation(predicate, arguments=arguments, query_function=self.common_query, write_function=self.common_write))

        return [
            [None, None]
        ]
