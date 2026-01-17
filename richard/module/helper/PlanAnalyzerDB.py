import sqlite3
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource


class PlanAnalyzerDB(Sqlite3DataSource):
    def __init__(self):

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE goal (event_id TEXT)")

        super().__init__(connection)


