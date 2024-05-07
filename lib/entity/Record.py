from __future__ import annotations
from dataclasses import dataclass


"""
A record represents a named tuple (row) in relation (table) of a database. This may be any type of database.
"""
@dataclass(frozen=True)
class Record:
    table: str
    values: dict

    def __init__(self, table: str, values: dict[str, int|float|str]):
        for name, value in values.items():
            if not name.isidentifier():
                raise Exception("The record key '" + name + "' is not an identier")
            if not isinstance(value, float) and not isinstance(value, str) and not isinstance(value, int):
                raise Exception("A record must be int, float or string")
        self.table = table
        self.values = values


    def subsetOf(self, other: Record):
        """
        This record is subsetOf other if other includes all name/values of this.
        """
        match = True
        for name, value in self.values.items():
            if name not in other.values or other.values[name] != value:
                match = False
        return match


