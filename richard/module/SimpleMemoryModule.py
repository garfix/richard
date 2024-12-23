import sqlite3
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.type.ExecutionContext import ExecutionContext


class SimpleMemoryModule(SomeModule):

    data_source: Sqlite3DataSource

    def __init__(self) -> None:
        super().__init__()
        self.clear()


    def clear(self):
        connection = sqlite3.connect(':memory:')
        self.data_source = Sqlite3DataSource(connection)


    def add_relation(self, relation: Relation):
        self.relations[relation.predicate] = relation
        relation.query_function = self.query
        relation.write_function = self.write


    def query(self, values: list, context: ExecutionContext) -> list[list]:
        return self.data_source.select(context.relation.predicate, context.relation.arguments, values)


    def write(self, values: list, context: ExecutionContext):
        self.data_source.insert(context.relation.predicate, context.relation.arguments, values)
