import unittest

from richard.data_source.PsycoPg2DataSource import PsycoPg2DataSource


class TestPostgresDB(unittest.TestCase):
    """
    To run this test, install psycopg2, set up a PostgreSQL database named "richard",
    create a table "customer" (with columns id and name) and fill it with (1, 'John') (2, 'Jack')
    """
   
    def test_psycopg2(self):


        # skip for now
        # return

        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor

            connection = psycopg2.connect(
                database='richard',
                host='127.0.0.1',
                user='patrick',
                password='test123',
                port=5432,
                # note: we won't use this cursor: the test is that it needs to be overridden by the default cursor
                cursor_factory=RealDictCursor
            )
        except ImportError:
            raise Exception("To run this test, import psycopg")
        
        ds = PsycoPg2DataSource(connection)

        self.assertEqual(ds.select_column('customer', ['id', 'name'], [None, None]), [1, 2])
        self.assertEqual(ds.select('customer', ['id', 'name'], [1, None]), [[1, 'John']])

        
