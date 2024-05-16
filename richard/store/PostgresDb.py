from richard.entity.Record import Record
from richard.entity.RecordSet import RecordSet
from richard.interface.SomeDb import SomeDb


class PostgresDb(SomeDb):
    """
    A record-based adapter to a PostgreSQL database
    """

    connection: any


    def __init__(self, connection) -> None:
        self.connection = connection


    def get_cursor(self):
        import psycopg2
        return self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


    def insert(self, record: Record):
        query = "INSERT INTO {} ({}) VALUES ({})".format(
            record.table,
            ",".join(record.values.keys()),
            ",".join(["%s" for v in record.values.values()])
        )
        self.get_cursor().execute(query, list(record.values.values()))
        self.connection.commit()


    def delete(self, record: Record):
        if record.is_empty():
            query = "DELETE FROM {}".format(record.table)
        else:
            query = "DELETE FROM {} WHERE {}".format(
                record.table,
                " AND ".join([key + "=%s" for key in record.values.keys()])
            )
        self.get_cursor().execute(query, list(record.values.values()))
        self.connection.commit()


    def select(self, record: Record) -> RecordSet:
        if record.is_empty():
            query = "SELECT * FROM {}".format(record.table)
        else:
            query = "SELECT * FROM {} WHERE {}".format(
                record.table,
                " AND ".join([key + "=%s" for key in record.values.keys()])
            )
        cursor = self.get_cursor()
        cursor.execute(query, list(record.values.values()))
        records = RecordSet()
        for row in cursor.fetchall():
            records.add(Record(record.table, dict(row)))
        return records
    
