from abc import ABC, abstractmethod

from richard.entity import Range


class SomeDataSource(ABC):
    """
    Implement this interface to give the library access to any type of data source be it an SQL database, NoSQL database, in-memory array or even CSV file.
    """
    @abstractmethod
    def select(self, table: str, columns: list[str], where: dict[str, any]) -> Range:
        """
            This method treats datasource access as were it a simple SQL SELECT statement:
            SELECT <columns>+ FROM <table> WHERE <where>*
            One or more columns (a, b, ...), zero or more where clauses (a=A AND b=B, ...)
        """
        pass
