from richard.interface.SomeDataSource import SomeDataSource


class MySqlDataSource(SomeDataSource):

    connection: any

    def __init__(self, connection):
        self.connection = connection


    def select(self, table: str, columns: list[str], values: list) -> list[list]:

        where = "TRUE"
        variables = []
        for column, value in zip(columns, values):
            if value is not None:
                where += f" AND {column}=%s"
                variables.append(value)

        cursor = self.connection.cursor()
        select = ','.join(columns)
        cursor.execute(f"SELECT {select} FROM {table} WHERE {where}", variables)
        return [list(row) for row in (cursor.fetchall())]
