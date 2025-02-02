import sqlite3
from richard.data_source.CsvImporter import CsvImporter
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource


class SIRDB(Sqlite3DataSource):
    # Using an in-memory sqlite database to store the facts
    def __init__(self):

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE isa (entity TEXT, type TEXT)")
        cursor.execute("CREATE TABLE identical (entity1 TEXT, entity2 TEXT)")
        cursor.execute("CREATE TABLE part_of (part TEXT, whole TEXT)")
        cursor.execute("CREATE TABLE part_of_n (part TEXT, whole TEXT, number INTEGER)")
        cursor.execute("CREATE TABLE own (person TEXT, thing TEXT)")
        cursor.execute("CREATE TABLE just_left_of (thing1 TEXT, thing2 TEXT)")
        cursor.execute("CREATE TABLE left_of (thing1 TEXT, thing2 TEXT)")

        super().__init__(connection)
