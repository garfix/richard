import csv
from richard.store.Record import Record
from richard.store.RecordSet import RecordSet


class MemoryDb:
    """
    A simple volatile data store. It indexes Records per table.
    """

    store: dict[str, list[Record]]


    def __init__(self) -> None:
        self.store = {}


    def insert(self, record: Record):
        if not record.table in self.store:
            self.store[record.table] = []

        self.store[record.table].append(record)


    def delete(self, record: Record):
        if not record.table in self.store:
            return

        records = []
        for r in self.store[record.table]:
            if not record.subsetOf(r):
                records.add(r)
        self.store[record.table] = records


    def select(self, record: Record) -> RecordSet:
        """
        returns all records from record's table that include record
        """
        result = RecordSet()

        if record.table in self.store:
            for r in self.store[record.table]:
                if record.subsetOf(r):
                    result.add(r)
        
        return result
    

    def import_csv(self, table: str, path: str):
        with open(path) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            line = 0
            headers = []
            for row in reader:
                if len(row) == 0:
                    continue
                line += 1
                if line == 1:
                    headers = row
                else:
                    values = {}
                    for header, element in zip(headers, row):
                        # a | implements an array of values
                        if "|" in element:
                            element = element.split("|")
                        # integer    
                        elif element.lstrip("-+").isdigit():
                            element = int(element)
                        values[header] = element
                        
                    self.insert(Record(table, values))
