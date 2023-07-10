from psycopg2.extensions import connection as psycopg2_connection
from tables.schemas import BaseTable
import itertools


def clear_table(connection: psycopg2_connection, table: BaseTable):
    table.create(connection=connection)
    table.drop(connection=connection)
    table.create(connection=connection)
    from connection.execute_query import execute_query

    cursor = execute_query(
        connection=connection,
        query=f"""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = '{table.name}';
""",
        return_cursor=True,
    )
    if isinstance(cursor, list):
        schema = [f"{d[0]}({d[1].upper()})" for d in cursor]
        print(
            f"\nCreated table '{table.name}' with the following columns:\n{', '.join(schema)}"
        )
