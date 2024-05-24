from richard.interface.SomeDataSource import SomeDataSource
from richard.store.MemoryDb import MemoryDb
from richard.store.Record import Record


class MemoryDbDataSource(SomeDataSource):

    db: MemoryDb

    def __init__(self, db: MemoryDb):
        self.db = db


    def select(self, table: str, columns: list[str], values: list[any]) -> list[list[any]]:
        where = {}
        for i, field in enumerate(values):
            if field is not None:
                column = columns[i]
                where[column] = field

        return self.db.select(Record(table, where)).fields(columns)
