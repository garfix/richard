from richard.interface.SomeDataSource import SomeDataSource
from richard.store.MemoryDb import MemoryDb
from richard.store.Record import Record


class MemoryDbDataSource(SomeDataSource):

    db: MemoryDb

    def __init__(self, db: MemoryDb):
        self.db = db


    def select(self, table: str, columns: list[str], where: dict[str, any]) -> list[list[any]]:
        return self.db.select(Record(table, where)).fields(columns)
