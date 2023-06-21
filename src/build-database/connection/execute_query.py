# =============================================================================
# SPSM SQL Query Execution
# =============================================================================
#
# Function to execute a given SQL query on the connected database
#
from psycopg2 import OperationalError
from psycopg2.extensions import connection as psycopg2_connection


def execute_query(connection: psycopg2_connection, query: str):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except OperationalError as e:
        print(f"The error {e} occured")
