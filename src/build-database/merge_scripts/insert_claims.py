from psycopg2.extensions import connection as psycopg2_connection

from merge_scripts.utils import Mapper
from utils import execute_query


def insert_data(
    connection: psycopg2_connection, data: Mapper, normalized_url_only: bool = False
):
    if normalized_url_only:
        columns_for_insert = (
            f"{data.source_table_id}, normalized_url, normalized_url_hash"
        )
        columns_for_select = f"id as {data.source_table_id}, {data.source_normalized_url} as normalized_url, {data.source_normalized_url_hash} as normalized_url_hash"
    else:
        columns_for_insert = f"{data.source_table_id}, normalized_url, normalized_url_hash, archive_url, title_from_html, title_from_web_archive, title_from_condor, title_from_youtube"
        columns_for_select = f"id as {data.source_table_id}, {data.source_normalized_url} as normalized_url, {data.source_normalized_url_hash} as normalized_url_hash, archive_url, title_from_html, title_from_web_archive, title_from_condor, title_from_youtube"

    query = f"""
INSERT INTO claims ({columns_for_insert})
SELECT {columns_for_select}
FROM {data.source_table_name}
WHERE NOT EXISTS( SELECT 1 FROM claims WHERE {data.source_table_id} = {data.source_table_name}.id)
        """
    execute_query(connection=connection, query=query)
