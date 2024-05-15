import unittest

from richard.entity.Record import Record


class TestPostgresDB(unittest.TestCase):
   
    def test_postgres(self):
        try:
            from richard.store.PostgresDb import PostgresDb
            db = PostgresDb('richard', 'patrick', 'test123')
        except:
            # psycopg not installed, Postgres not installed, no database "richard" created or table "customer" not created: skip test
            return
        
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


