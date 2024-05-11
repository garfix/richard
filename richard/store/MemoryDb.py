from richard.entity.Record import Record
from richard.entity.RecordSet import RecordSet


class MemoryDb:
    """
    A simple volatile data store. It indexes Records per table.
    """

    store: dict[str, list[Record]]


    def __init__(self) -> None:
        self.store = {}


    def assert_record(self, record: Record):
        if not record.table in self.store:
            self.store[record.table] = []

        self.store[record.table].append(record)


    def match(self, record: Record) -> RecordSet:
        """
        returns all records from record's table that include record
        """
        result = RecordSet()

        if record.table in self.store:
            for r in self.store[record.table]:
                if record.subsetOf(r):
                    result.add(r)
        
        return result
    
