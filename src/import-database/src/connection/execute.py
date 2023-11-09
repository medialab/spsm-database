from psycopg2.extensions import connection as Connection


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
        print(f"\nquery: {query}")
        print(f"values: {values}")
        print(f"The error {e} occured")
        raise e
    else:
        if return_cursor:
            return cursor.fetchall()
