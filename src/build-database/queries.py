from psycopg2 import OperationalError
from psycopg2.extensions import connection as psycopg2_connection


def execute_query(connection: psycopg2_connection, query: str):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query successfully executed")
    except OperationalError as e:
        print(f"The error {e} occured")


def drop_table(connection: psycopg2_connection, table_name: str):
    query = f"DROP TABLE IF EXISTS {table_name};"
    execute_query(connection, query)


def create_table(connection: psycopg2_connection, table_name: str, table_schema: list):
    schema = ", ".join(table_schema)
    query = f"CREATE TABLE IF NOT EXISTS {table_name}({schema});"
    execute_query(connection, query)


def insert(connection: psycopg2_connection, table_name: str, values: list):
    schema = ", ".join([f"'{value}'" for value in values])
    query = f"INSERT INTO {table_name} VALUES ({schema});"
    execute_query(connection, query)
