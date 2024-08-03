import csv
from richard.store.Record import Record


class MemoryDb:
    """
    A simple volatile data store. It indexes Records per table.
    """

    store: dict[str, list[Record]]
    index: dict[dict[set[Record]]]


    def __init__(self) -> None:
        self.store = {}
        self.index = {}


    def insert(self, record: Record):

        # per table store

        if not record.table in self.store:
            self.store[record.table] = []

        self.store[record.table].append(record)

        # per value index

        if not record.table in self.index:
            self.index[record.table] = {}

        for key, value in record.values.items():

            value = str(value)

            if not key in self.index[record.table]:
                self.index[record.table][key] = {}

            if not value in self.index[record.table][key]:
                self.index[record.table][key][value] = set()

            self.index[record.table][key][value].add(record)


    def delete(self, record: Record):
        if not record.table in self.store:
            return

        records = []
        for r in self.store[record.table]:
            if not record.subsetOf(r):
                records.add(r)
        self.store[record.table] = records


    def select(self, table, values: dict) -> list:
        """
        returns all records from record's table that include record
        """
        if not table in self.index:
            return []

        if values == {}:
            return self.store[table]

        # create a separate set of records for each element in the record's values
        sets = []
        for key, value in values.items():
            value = str(value)
            if key in self.index[table] and value in self.index[table][key]:
                sets.append(self.index[table][key][value])
            else:
                return []
                       
        # return the intersection of these sets                       
        return set.intersection(*sets)
    

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
