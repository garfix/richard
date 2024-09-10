from richard.data_source.MemoryDbDataSource import MemoryDbDataSource
from richard.entity.Relation import Relation
from richard.interface.SomeDataSource import SomeDataSource
from richard.interface.SomeModule import SomeModule
from richard.store.MemoryDb import MemoryDb


class Chat80SentenceContext(SomeModule):
    
    ds: SomeDataSource


    def __init__(self) -> None:
        self.ds = MemoryDbDataSource(MemoryDb())

        self.relations = {
            "format": Relation(attributes=["type", "variables", "units"], writable=True),
        }

