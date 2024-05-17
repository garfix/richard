from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Record:
    """
    A record represents a named tuple (row) in relation (table) of a database. This may be any type of database.
    """

    table: str
    # default: empty dictionary
    values: dict[str, int|float|str] = field(default_factory=dict)


    def __post_init__(self):
        for name, value in self.values.items():
            if not name.isidentifier():
                raise ValueError("The record key '" + name + "' is not an identier")
            if not isinstance(value, float) and not isinstance(value, str) and not isinstance(value, int):
                raise ValueError("A record must be int, float or string")
    

    def __str__(self):
        return self.table + " " + str(self.values)
    

    def is_empty(self) -> bool:
        return len(self.values) == 0


    def __hash__(self) -> int:
        # see https://stackoverflow.com/a/5884123
        return hash(self.table) + hash(frozenset(self.values.items()))


    def subsetOf(self, other: Record):
        """
        This record is subsetOf other if other includes all name/values of this.
        """
        match = True
        for name, value in self.values.items():
            if name not in other.values or other.values[name] != value:
                match = False
        return match


