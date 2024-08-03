from __future__ import annotations
from dataclasses import dataclass, field


class Record:
    """
    A record represents a named tuple (row) in relation (table) of a database. This may be any type of database.
    """

    table: str
    values: dict
    hash: int

    def __init__(self, table: str, values: dict):
        self.table = table
        self.values = values
        
        for name, value in self.values.items():
            if not name.isidentifier():
                raise ValueError("The record key '" + name + "' is not an identier")
            if not isinstance(value, float) and not isinstance(value, str) and not isinstance(value, int) and not isinstance(value, list):
                raise ValueError("A record must be int, float or string: " + str(value))
            
        h = []
        for key, value in values.items():
            h.append(key)
            if isinstance(value, list):
                h.extend(value)
            else:
                h.append(value)
        self.hash = hash(tuple(h))
    

    def __str__(self):
        return self.table + " " + str(self.values)
    

    def is_empty(self) -> bool:
        return len(self.values) == 0


    def __hash__(self) -> int:
        return self.hash


    def subsetOf(self, other: Record):
        """
        This record is subsetOf other if other includes all name/values of this.
        """
        match = True
        for name, value in self.values.items():
            if name not in other.values or other.values[name] != value:
                match = False
        return match


