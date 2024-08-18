from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Relation import Relation
from richard.interface.SomeModule import SomeModule
from richard.store.MemoryDb import MemoryDb
from richard.type.ExecutionContext import ExecutionContext


class SimpleMemoryModule(SomeModule):

    ds: MemoryDbDataSource

    def __init__(self, relations: dict[str, Relation]) -> None:
        self.ds = MemoryDbDataSource(MemoryDb())
        self.relations = relations

        for _, relation in relations.items():
            relation.query_function = self.query
            relation.write_function = self.write


    def query(self, values: list, context: ExecutionContext) -> list[list]:
        return self.ds.select(context.predicate, context.relation.attributes, values)


    def write(self, values: list, context: ExecutionContext):
        self.ds.insert(context.predicate, context.relation.attributes, values)


    def clear(self):
        self.ds.clear()
