import pathlib
import sqlite3
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource


class PAMDB(Sqlite3DataSource):
    # Using an in-memory sqlite database to store Hello world's facts
    def __init__(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE entity (id TEXT, name TEXT)")

        super().__init__(connection)


