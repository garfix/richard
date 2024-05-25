from richard.interface.SomeDataSource import SomeDataSource
from richard.type.Simple import Simple


class PsycoPg2DataSource(SomeDataSource):

    connection: any

    def __init__(self, connection):
        self.connection = connection


    def select(self, table: str, columns: list[str], values: list[Simple]) -> list[list[Simple]]:

        import psycopg2

        where = "TRUE"
        variables = []
        for column, value in zip(columns, values):
            if value is not None:
                where += f" AND {column}=%s"
                variables.append(value)

        cursor = self.connection.cursor(cursor_factory=psycopg2.extensions.cursor)
        select = ','.join(columns)
        cursor.execute(f"SELECT {select} FROM {table} WHERE {where}", variables)
        return [list(row) for row in (cursor.fetchall())]
    