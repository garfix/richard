from abc import ABC, abstractmethod



class SomeDataSource(ABC):
    """
    Implement this interface to give the library access to any type of data source be it an SQL database, NoSQL database, in-memory array or even CSV file.
    """
    @abstractmethod
    def select(self, table: str, columns: list[str], values: list) -> list[list]:
        """
            This method treats datasource access as were it a simple SQL SELECT statement:
            SELECT <columns>+ FROM <table> WHERE <column>=<value>*
            One or more columns (column1, column1, ...), zero or more where clauses (columns1=values1 AND columns1=values1, ...)
            Note that same columns are both used in the "select" and the "where"
            Note that if a value is None, it must be omitted from the "where"
        """
        pass


    def select_column(self, table: str, columns: list[str], values: list) -> list:
        return [row[0] for row in self.select(table, columns, values)]


    def insert(self, table: str, columns: list[str], values: list):
        pass
