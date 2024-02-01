import logging
from typing import List

from psycopg2.extensions import connection as Connection

logging.basicConfig(
    filemode="w", filename="postgres.log", encoding="utf-8", level=logging.ERROR
)


def execute_query(
    connection: Connection,
    query: str,
    values: tuple | None = None,
    return_cursor: bool = False,
) -> None | List | Exception:
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
    except Exception as e:
        msg = f"\nquery: {query}\nvalues: {values}\nThe error {e} occured"
        logging.error(msg=msg)
        return e
    else:
        if return_cursor:
            return cursor.fetchall()
