from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.store.Record import Record
from richard.store.MemoryDb import MemoryDb


class MemoryDbDataSource(SomeDataSource):

    db: MemoryDb

    def __init__(self, db: MemoryDb):
        self.db = db


    def select(self, table: str, columns: list[str], values: list) -> list[list]:

        # from list to dictionary
        where = {}
        for field, column in zip(values, columns):
            if field is not None:
                where[column] = field

        # call db
        records = self.db.select(table, where)

        # from records to lists
        result = []
        for record in records:
            values = [record.values[column] for column in columns]
            result.append(values)
        return result


    def insert(self, table: str, columns: list[str], values: list):
        self.db.insert(Record(table, dict(zip(columns, values))))


    def clear(self):
        self.db.clear()