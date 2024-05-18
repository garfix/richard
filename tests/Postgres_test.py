import unittest

from richard.Domain import Domain
from richard.entity.Entity import Entity


class TestPostgresDB(unittest.TestCase):
    """
    To run this test, install psycopg2, set up a PostgreSQL database named "richard",
    create a table "customer" (with columns id and name) and fill it with (1, 'John') (2, 'Jack')
    """
   
    def test_postgres(self):


        # skip for now
        return

        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor

            connection = psycopg2.connect(
                database='richard',
                host='127.0.0.1',
                user='patrick',
                password='test123',
                port=5432,
                cursor_factory=RealDictCursor
            )
        except ImportError:
            raise Exception("To run this test, import psycopg")
        
        def get_all_ids(table: str):
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM " + table)
            return [row['id'] for row in cursor.fetchall()]

        domain = Domain([
            Entity('customer', lambda: get_all_ids('customer'))
        ], [])

        self.assertEqual(domain.get_entity_ids('customer'), [1, 2])

        
