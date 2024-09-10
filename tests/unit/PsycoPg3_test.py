import unittest

from richard.data_source.PsycoPg3DataSource import PsycoPg3DataSource


class TestPsycoPg3(unittest.TestCase):
    """
    To run this test, install PostgreSQL, set up a PostgreSQL database named "richard" and perform

    create table customer (id int, name text);
    insert into customer (id, name) values (1, 'John'), (2, 'Jack');

    A Python package to access Postgres is needed

    pip install "psycopg[binary]"

    """

    def test_psycopg3(self):


        # skip for now
        return

        try:
            import psycopg

            with psycopg.connect(
                dbname='richard', # Your database
                host='127.0.0.1',
                user='patrick', # Your username
                password='test123', # Your password
                port=5432
            ) as connection:

                ds = PsycoPg3DataSource(connection)

                self.assertEqual(ds.select_column('customer', ['id', 'name'], [None, None]), [1, 2])
                self.assertEqual(ds.select('customer', ['id', 'name'], [1, None]), [[1, 'John']])

        except ImportError:
            raise Exception("To run this test, import psycopg3")



