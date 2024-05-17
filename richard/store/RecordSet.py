from richard.store.Record import Record


class RecordSet:
    """
    A record set is a set of records: each record can appear only once 
    """
    
    # each record can occur only once
    _records: set[Record]


    def __init__(self) -> None:
        self._records = set()


    def __len__(self) -> int:
        return len(self._records)


    def add(self, record: Record):
        self._records.add(record)


    # make the set iterable
    def __iter__(self):
        for record in self._records:
            yield record

    
    def field(self, field: str) -> list:
        """
        Returns a list with all distinct values of field
        """
        values = set()
        for record in self._records:
            if field in record.values:
                values.add(record.values[field])
        return list(values)
