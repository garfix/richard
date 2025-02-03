import pathlib
import sqlite3
from richard.data_source.CsvImporter import CsvImporter
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource


class HellowWorldDB(Sqlite3DataSource):
    # Using an in-memory sqlite database to store Hello world's facts
    def __init__(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE river (id TEXT PRIMARY KEY, flows_through TEXT)")

        super().__init__(connection)

        csv_importer = CsvImporter()
        csv_importer.import_table_from_file('river', path + "resources/river.csv", self)

