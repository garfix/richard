import unittest
from richard.data_source.Sqlite3DataSource import Sqlite3DataSource
from richard.entity.Variable import Variable


class TestSqlite3(unittest.TestCase):
    """
    Tests using Sqlite3
    """

    def test_sqlite3(self):

        import sqlite3

        # create a database (in memory)
        connection = sqlite3.connect(':memory:')
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

        ds = Sqlite3DataSource(connection)

        self.assertEqual(ds.select_column('customer', ['id', 'name'], [Variable('E1'), Variable('E2')]), [1, 2])
        self.assertEqual(ds.select('customer', ['id', 'name'], [1, Variable('E1')]), [[1, 'John']])


