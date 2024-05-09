from __future__ import annotations
from dataclasses import dataclass


class Record:
    """
    A record represents a named tuple (row) in relation (table) of a database. This may be any type of database.
    """

    _table: str
    _values: dict[str, int|float|str]

    def __init__(self, table: str, values: dict[str, int|float|str]):
        for name, value in values.items():
            if not name.isidentifier():
                raise ValueError("The record key '" + name + "' is not an identier")
            if not isinstance(value, float) and not isinstance(value, str) and not isinstance(value, int):
                raise ValueError("A record must be int, float or string")
        self._table = table
        self._values = values


    @property
    def table(self):
        return self._table


    @property
    def values(self):
        return self._values


    def subsetOf(self, other: Record):
        """
        This record is subsetOf other if other includes all name/values of this.
        """
        match = True
        for name, value in self._values.items():
            if name not in other._values or other._values[name] != value:
                match = False
        return match


