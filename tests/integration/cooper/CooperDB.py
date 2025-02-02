import sqlite3
from richard.data_source.CsvImporter import CsvImporter
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource


class CooperDB(Sqlite3DataSource):
    # Using an in-memory sqlite database to store the facts
    def __init__(self):

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()

        # note: same entity may have multiple names
        cursor.execute("CREATE TABLE entity (id TEXT, name TEXT)")

        cursor.execute("CREATE TABLE metal (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE element (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE compound (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE nonmetal (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE white (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE dark_gray (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE brittle (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE oxide (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE sulfide (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE chloride (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE fuel (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE burns (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE burns_rapidly (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE combustable (entity TEXT PRIMARY KEY, truth TEXT)")
        cursor.execute("CREATE TABLE gasoline (entity TEXT PRIMARY KEY, truth TEXT)")

        super().__init__(connection)
