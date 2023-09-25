import csv
import gzip
from typing import Generator
from pathlib import Path

import psycopg2
import psycopg2.extensions
from psycopg2 import OperationalError
from psycopg2.extensions import connection as psycopg2_connection


def connect_to_database(yaml):
    config = {
        "db_name": None,
        "db_user": None,
        "db_password": None,
        "db_port": None,
        "db_host": None,
    }
    config.update(yaml["connection"])
    connection = None
    try:
        connection = psycopg2.connect(
            database=config["db_name"],
            user=config["db_user"],
            password=config["db_password"],
            host=config["db_host"],
            port=config["db_port"],
        )
        print("Connection to PostgreSQL DB successful.")
    except OperationalError as e:
        print(f"The error {e} occured.")
    return connection


def execute_query(
    connection: psycopg2_connection,
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


def count_table_rows(connection: psycopg2_connection, table_name: str) -> int:
    query = "SELECT count(*) from %s" % table_name
    cursor_result = execute_query(
        connection=connection, query=query, return_cursor=True
    )
    if isinstance(cursor_result, list) and isinstance(cursor_result[0][0], int):
        return cursor_result[0][0]
    else:
        raise TypeError


def yield_csv_dict_row(file) -> Generator[dict, None, None]:
    if Path(file).is_file():
        try:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield row
        except UnicodeDecodeError:
            with gzip.open(file, "rt") as f:
                reader = csv.DictReader(f)  # type: ignore
                for row in reader:
                    yield row
