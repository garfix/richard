from richard.entity.Variable import Variable
from richard.interface.SomeDataSource import SomeDataSource
from richard.store.MemoryDb import MemoryDb
from richard.type.Simple import Simple


class MemoryDbDataSource(SomeDataSource):

    db: MemoryDb

    def __init__(self, db: MemoryDb):
        self.db = db


    def select(self, table: str, columns: list[str], values: list[Simple]) -> list[list[Simple]]:

        # from list to dictionary
        where = {}
        for field, column in zip(values, columns):
            if field is not None and not isinstance(field, Variable):
                where[column] = field

        # call db
        records = self.db.select(table, where)

        # from records to lists
        result = []
        for record in records:
            values = []
            for field in columns:
                values.append(record.values[field])
            result.append(values)
        return result

