from richard.interface.SomeDataSource import SomeDataSource


class SimpleDataSource(SomeDataSource):
    """
    A simple data store, useful for small amounts of data.
    Doesn't care about data types, which means they can contain lists etc
    """

    store: dict[str, list[dict]]


    def __init__(self) -> None:
        self.clear()


    # def insert(self, record: Record):
    def insert(self, table: str, columns: list[str], values: list):

        values = self.create_dict(columns, values)

        if not table in self.store:
            self.store[table] = []

        self.store[table].append(values)


    # def select(self, table, values: dict) -> list:
    def select(self, table: str, columns: list[str], list_values: list) -> list[list]:

        values = self.create_dict(columns, list_values)

        if not table in self.store:
            return []

        results = []

        for record in self.store[table]:
            ok = True
            for key, value in values.items():
                if key in record:
                    if record[key] != value:
                        ok = False
            if ok:
                result = [record[column] for column in columns]
                results.append(result)

        return results


    def clear(self):
        self.store = {}


    def create_dict(self, columns: list, values: list):
        d = {}
        for key, val in zip(columns, values):
            if val is not None:
                d[key] = val
        return d