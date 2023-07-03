from psycopg2.extensions import connection as psycopg2_connection
from tables.schemas import BaseTable


def clear_table(connection: psycopg2_connection, table: BaseTable):
    table.create(connection=connection)
    table.drop(connection=connection)
    table.create(connection=connection)
