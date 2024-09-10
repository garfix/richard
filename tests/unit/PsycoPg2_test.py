import unittest

from richard.data_source.PsycoPg2DataSource import PsycoPg2DataSource


class TestPsycopPg2(unittest.TestCase):
    """
    To run this test, install PostgreSQL, set up a PostgreSQL database named "richard" and perform

    create table customer (id int, name text);
    insert into customer (id, name) values (1, 'John'), (2, 'Jack');

    A Python package to access Postgres is needed

    pip install psycopg2-binary

    """

    def test_psycopg2(self):


        # skip for now
        return

        try:
            import psycopg2

            connection = psycopg2.connect(
                database='richard', # Your database
                host='127.0.0.1',
                user='patrick', # Your username
                password='test123', # Your password
                port=5432
            )
        except ImportError:
            raise Exception("To run this test, import psycopg2")

        ds = PsycoPg2DataSource(connection)

        self.assertEqual(ds.select_column('customer', ['id', 'name'], [None, None]), [1, 2])
        self.assertEqual(ds.select('customer', ['id', 'name'], [1, None]), [[1, 'John']])


