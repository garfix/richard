import unittest

from richard.data_source.PsycoPg2DataSource import PsycoPg2DataSource


class TestPostgresDB(unittest.TestCase):
    """
    To run this test, install PostgreSQL, set up a PostgreSQL database named "richard" and perform

    create table customer (id int, name text);
    insert into customer (id, name) values (1, 'John'), (2, 'Jack');

    A Python package (PsycoPg 2 or 3) to access Postgres is needed

    pip install psycopg2-binary

    """

    def test_psycopg2(self):


        # skip for now
        return

        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor

            connection = psycopg2.connect(
                database='richard', # Your Postgres database
                host='127.0.0.1',
                user='patrick', # Your Postgres username
                password='test123', # Your MySQL password
                port=5432,
                # note: we won't use this cursor: the test is that it will to be overridden by the default cursor
                cursor_factory=RealDictCursor
            )
        except ImportError:
            raise Exception("To run this test, import psycopg")

        ds = PsycoPg2DataSource(connection)

        self.assertEqual(ds.select_column('customer', ['id', 'name'], [None, None]), [1, 2])
        self.assertEqual(ds.select('customer', ['id', 'name'], [1, None]), [[1, 'John']])


