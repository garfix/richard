import pathlib
import unittest
from richard.data_source.SqliteDataSource import SqliteDataSource


class TestSqlite3(unittest.TestCase):
    """
    Tests using Sqlite3
    """

    def test_sqlite3(self):

        import sqlite3

        path = str(pathlib.Path(__file__).parent.resolve()) + "/sqlite3/"

        # Creates 'richard.db' if it doesn't exist
        connection = sqlite3.connect(path + 'richard.db')
        cursor = connection.cursor()

        # create a table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)

        # insert some values
        try:
            cursor.execute("INSERT INTO customer (id, name) VALUES (1, 'John'), (2, 'Jack')")
        except:
            pass

        connection.commit()

        ds = SqliteDataSource(connection)

        self.assertEqual(ds.select_column('customer', ['id', 'name'], [None, None]), [1, 2])
        self.assertEqual(ds.select('customer', ['id', 'name'], [1, None]), [[1, 'John']])


