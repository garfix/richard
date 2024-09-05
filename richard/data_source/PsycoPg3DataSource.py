from richard.interface.SomeDataSource import SomeDataSource


class PsycoPg3DataSource(SomeDataSource):

    connection: any

    def __init__(self, connection):
        self.connection = connection


    def select(self, table: str, columns: list[str], values: list) -> list[list]:

        import psycopg

        where = "TRUE"
        variables = []
        for column, value in zip(columns, values):
            if value is not None:
                where += f" AND {column}=%s"
                variables.append(value)

        cursor = self.connection.cursor(row_factory=psycopg.rows.tuple_row)
        select = ','.join(columns)
        cursor.execute(f"SELECT {select} FROM {table} WHERE {where}", variables)
        return [list(row) for row in (cursor.fetchall())]
