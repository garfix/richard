import unittest

from richard.data_source.MySqlDataSource import MySqlDataSource


class TestPostgresDB(unittest.TestCase):
    """
    To run this test, install MySQL, set up a MySQL database named "richard" and perform

    create table customer (id int, name text);
    insert into customer (id, name) values (1, 'John'), (2, 'Jack');

    A Python package to access MySQL is needed

    pip install mysql-connector-python

    """

    def test_mysql(self):


        # skip for now
        # return

        try:
            import mysql.connector

            connection = mysql.connector.connect(
                host="localhost",
                user="patrick",  # Your MySQL username
                password="test123",  # Your MySQL password
                database="richard"  # Your database name
            )

        except ImportError:
            raise Exception("To run this test, import mysql")

        ds = MySqlDataSource(connection)

        self.assertEqual(ds.select_column('customer', ['id', 'name'], [None, None]), [1, 2])
        self.assertEqual(ds.select('customer', ['id', 'name'], [1, None]), [[1, 'John']])


