from richard.entity.Relation import Relation
from richard.module.SimpleMemoryModule import SimpleMemoryModule
from richard.type.ExecutionContext import ExecutionContext


class BasicDialogContext(SimpleMemoryModule):

    def __init__(self) -> None:
        super().__init__()

        self.clear()

        self.add_relation(Relation("dialog_isa", arguments=["entity", "type"]))
        self.add_relation(Relation("context", arguments=["name"]))

        self.add_relation(Relation("with_context", arguments=["name", "body"], query_function=self.with_context))
        self.add_relation(Relation("start_context", arguments=["name"], query_function=self.start_context))
        self.add_relation(Relation("end_context", arguments=["name"], query_function=self.end_context))


    def with_context(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0]
        body = values[1]
        self.data_source.insert('context', ['name'], [name])
        context.solver.solve(body, context.binding)
        self.data_source.delete('context', ['name'], [name])
        return [
            [None, None]
        ]

    def start_context(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0]
        self.data_source.insert('context', ['name'], [name])
        return [
            [None]
        ]


    def end_context(self, values: list, context: ExecutionContext) -> list[list]:
        name = values[0]
        self.data_source.delete('context', ['name'], [name])
        return [
            [None]
        ]


    def clear(self):
        super().clear()

        cursor = self.data_source.connection.cursor()

        cursor.execute("CREATE TABLE dialog_isa (entity TEXT, type TEXT)")
        cursor.execute("CREATE TABLE context (name TEXT)")
