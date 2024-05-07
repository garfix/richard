from lib.entity.Record import Record


class MemoryDb:
    """
    A simple volatile data store. It indexes Records per table.
    """

    store: dict[str, list[Record]]


    def __init__(self) -> None:
        self.store = {}


    def assert_record(self, relation: str, record: Record):
        if not relation in self.store:
            self.store[relation] = []

        self.store[relation].append(record)


    def match(self, record: Record) -> list[Record]:
        """
        returns all records from record's table that include record
        """
        result = []

        if record.table in self.store:
            for r in self.store[record.table]:
                if record.subsetOf(r):
                    result.append(r)
        
        return result
    
