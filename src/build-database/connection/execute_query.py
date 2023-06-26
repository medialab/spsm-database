# =============================================================================
# SPSM SQL Query Execution
# =============================================================================
#
# Function to execute a given SQL query on the connected database
#
from psycopg2.extensions import connection as psycopg2_connection


def execute_query(
    connection: psycopg2_connection,
    query: str,
    values: tuple | None = None,
    return_cursor: bool = False,
):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
    except Exception as e:
        print(f"\nquery: {query}")
        print(f"values: {values}")
        print(f"The error {e} occured")
        raise e
    else:
        if return_cursor:
            return cursor.fetchall()
