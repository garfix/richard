from richard.interface.SomeDataSource import SomeDataSource


class Sqlite3DataSource(SomeDataSource):

    connection: any

    def __init__(self, connection):
        self.connection = connection


    def select(self, table: str, columns: list[str], values: list) -> list[list]:

        where = "TRUE"
        variables = []
        for column, value in zip(columns, values):
            if value is not None:
                where += f" AND {column}=?"
                variables.append(value)

        cursor = self.connection.cursor()
        select = ','.join(columns)
        cursor.execute(f"SELECT {select} FROM {table} WHERE {where}", variables)
        return [list(row) for row in (cursor.fetchall())]


    def insert(self, table: str, columns: list[str], values: list):
        cursor = self.connection.cursor()
        column_string = ','.join(columns)
        place_holders = ", ".join(['?' for v in values])
        cursor.execute(f"INSERT OR IGNORE INTO {table} ({column_string}) VALUES ({place_holders})", values)


    def delete(self, table: str, columns: list[str], values: list):
        cursor = self.connection.cursor()
        place_holders = "AND ".join([f'{c} = ? ' for c in columns])
        cursor.execute(f"DELETE FROM {table} WHERE {place_holders}", values)


    def clear(self):
        raise Exception('clear not implemented')
