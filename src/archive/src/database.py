import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

import psycopg2
import psycopg2.extensions
from psycopg2 import OperationalError
from psycopg2.extensions import connection as psycopg2_connection

from constants import POSTGRES_TABLE_NAME


class PostgresWrapper:
    def __init__(self, yaml: Dict) -> None:
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
            print("\n================================")
            print("Connection to PostgreSQL DB successful.")
        except OperationalError as e:
            print(f"The error {e} occured.")
        self.connection = connection

    def insert(
        self,
        url_id: str,
        archive_url: str,
        archive_timestamp: datetime | None,
        archive_html_file: Path | None,
        archive_view_url: str | None,
    ):
        screen_id = os.environ.get("STY")
        if archive_html_file:
            archive_html_file = str(archive_html_file.absolute())
        values = (
            url_id,
            archive_url,
            archive_timestamp,
            archive_html_file,
            archive_view_url,
            screen_id,
        )

        query = f"""
INSERT INTO "{POSTGRES_TABLE_NAME}" (url_id, archive_url, archive_timestamp_utc, archive_html_file, archive_view_uri, screen_id)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (url_id)
DO UPDATE SET
    archive_url = excluded.archive_url,
    archive_timestamp_utc = coalesce(excluded.archive_timestamp_utc, "{POSTGRES_TABLE_NAME}".archive_timestamp_utc),
    archive_html_file = coalesce(excluded.archive_html_file, "{POSTGRES_TABLE_NAME}".archive_html_file),
    archive_view_uri = coalesce(excluded.archive_view_uri, "{POSTGRES_TABLE_NAME}".archive_view_uri),
    screen_id = excluded.screen_id
        """

        self.execute_query(query=query, values=values)

    def execute_query(
        self,
        query: str,
        values: Tuple | None = None,
        return_cursor: bool = False,
    ) -> None | list:
        if not isinstance(self.connection, psycopg2_connection):
            raise OperationalError
        self.connection.autocommit = True
        cursor = self.connection.cursor()
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
