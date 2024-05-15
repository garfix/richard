from richard.entity.Record import Record
from richard.entity.RecordSet import RecordSet
from richard.interface.SomeDb import SomeDb

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    raise Exception("To use class PostgresDb import psycopg2: pip install psycopg2-binary")


class PostgresDb(SomeDb):
    """
    A record-based adapter to a PostgreSQL database
    """

    connection: psycopg2.extensions.connection


    def __init__(self, database: str, user: str, password: str, host: str='127.0.0.1', port: int=5432) -> None:
        self.connection = psycopg2.connect(
            database=database,
            host=host,
            user=user,
            password=password,
            port=port,
            cursor_factory=RealDictCursor
        )

    def get_cursor(self) -> RealDictCursor:
        return self.connection.cursor()


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
    
