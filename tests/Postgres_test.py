import unittest

from richard.entity.Record import Record
from richard.store.PostgresDb import PostgresDb


class TestPostgresDB(unittest.TestCase):
   
    def test_postgres(self):
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor

            connection = psycopg2.connect(
                database='richard',
                host='127.0.0.1',
                user='patrick',
                password='test123',
                port=5432
            )
        except ImportError:
            raise Exception("To use class PostgresDb import package psycopg")

        db = PostgresDb(connection)
        
        # insert
        db.insert(Record('customer', {'id': 1, 'name': 'Jones'}))
        db.insert(Record('customer', {'id': 2, 'name': 'Jackson'}))
        db.insert(Record('customer', {'id': 3, 'name': 'Dodge'}))

        # select
        for row in db.select(Record('customer', {'id': 1})):
            self.assertEqual(row.values['name'], 'Jones')

        for row in db.select(Record('customer', {'name': 'Jackson'})):
            self.assertEqual(row.values['id'], 2)
                         
        # delete
        db.delete(Record('customer', {'id': 1}))
        self.assertEqual(len(db.select(Record('customer'))), 2)

        db.delete(Record('customer'))
        self.assertEqual(len(db.select(Record('customer'))), 0)


