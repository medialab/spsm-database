import logging

from psycopg2.extensions import connection as Connection

logging.basicConfig(filemode="w", filename="postgres.log")


def execute_query(
    connection: Connection,
    query: str,
    values: tuple | None = None,
    return_cursor: bool = False,
) -> None | list:
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
    except Exception as e:
        msg = f"\nquery: {query}\nvalues: {values}\nThe error {e} occured"
        print(msg)
        logging.log(level=1, msg=msg)
        raise e
    else:
        if return_cursor:
            return cursor.fetchall()
