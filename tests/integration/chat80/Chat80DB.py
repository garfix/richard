import pathlib
import sqlite3
from richard.data_source.CsvImporter import CsvImporter
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource


class Chat80DB(Sqlite3DataSource):
    # Using an in-memory sqlite database to store Chat-80's facts
    def __init__(self):

        path = str(pathlib.Path(__file__).parent.resolve()) + "/"

        connection = sqlite3.connect(':memory:')
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE continent (id TEXT PRIMARY KEY)")
        cursor.execute("CREATE TABLE ocean (id TEXT PRIMARY KEY)")
        cursor.execute("CREATE TABLE sea (id TEXT PRIMARY KEY)")
        cursor.execute("CREATE TABLE river (id TEXT PRIMARY KEY, flows_through TEXT)")
        cursor.execute("CREATE TABLE city (id TEXT PRIMARY KEY, country TEXT, population INTEGER)")
        cursor.execute("""
                       CREATE TABLE country (
                        id TEXT PRIMARY KEY,
                        region TEXT, capital TEXT, currency TEXT,
                        lat REAL, long REAL,
                        area_div_1000 INTEGER, area_mod_1000 INTEGER,
                        population INTEGER, population_mod_1000000_div_1000 INTEGER
                    )""")
        cursor.execute("CREATE TABLE contains (whole TEXT, part TEXT)")
        cursor.execute("CREATE TABLE borders (country_id1 TEXT, country_id2 TEXT)")

        cursor.execute("CREATE INDEX borders_country_id1 ON borders (country_id1)")
        cursor.execute("CREATE INDEX borders_country_id2 ON borders (country_id2)")
        cursor.execute("CREATE INDEX contains_whole ON contains (whole)")
        cursor.execute("CREATE INDEX contains_part ON contains (part)")

        super().__init__(connection)

        csv_importer = CsvImporter()
        csv_importer.import_table_from_file('continent', path + "resources/continent.csv", self)
        csv_importer.import_table_from_file('ocean', path + "resources/ocean.csv", self)
        csv_importer.import_table_from_file('sea', path + "resources/sea.csv", self)
        csv_importer.import_table_from_file('river', path + "resources/river.csv", self)
        csv_importer.import_table_from_file('city', path + "resources/city.csv", self)
        csv_importer.import_table_from_file('country', path + "resources/country.csv", self)
        csv_importer.import_table_from_file('contains', path + "resources/contains.csv", self)
        csv_importer.import_table_from_file('borders', path + "resources/borders.csv", self)
