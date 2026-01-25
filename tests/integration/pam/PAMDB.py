import sqlite3
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource


class PAMDB(Sqlite3DataSource):
    def __init__(self):

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE entity (id TEXT, name TEXT)")
        cursor.execute("CREATE TABLE lost (id TEXT)")
        cursor.execute("CREATE TABLE name (name TEXT, id TEXT)")
        cursor.execute("CREATE TABLE male (id TEXT)")
        cursor.execute("CREATE TABLE person (id TEXT)")

        super().__init__(connection)
