# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for inserting original data sources into SQL tables
#
from connection.execute_query import execute_query
from psycopg2.extensions import connection as psycopg2_connection
from utils import clear_table
from tables.schemas import (
    BaseTable,
    CompletedURLDatasetTable,
    CompletedURLsTable,
    ClaimTable,
    CondorTable,
    DeFactoTable,
    ScienceFeedbackTable,
    EnrichedURLTitleDataset,
)


def insert_data_sources(connection: psycopg2_connection):
    # Add enriched titles to each item in the data source tables
    # add_titles_to_data_sources(connection=connection)
    # Create claim table
    create_claim_table(connection=connection)


def create_claim_table(connection: psycopg2_connection):
    titles = EnrichedURLTitleDataset()
    html_title = titles.title_from_html.name
    archive_title = titles.title_from_webarchive.name
    yt_title = titles.title_from_youtube.name

    claim_table = ClaimTable()
    clear_table(connection=connection, table=claim_table)

    # Insert first values into claim table
    c = CondorTable()
    query = f"""
    INSERT INTO {claim_table.name}
    SELECT COALESCE({c.name}.{c.share_title.name}, '') as title, {c.name}.{c.normalized_url.name}, ARRAY_AGG ({c.name}.{c.id.name}) AS condor_id
    FROM {c.name}
    GROUP BY ({c.name}.{c.share_title.name}, {c.name}.{c.normalized_url.name})
    """
    execute_query(connection=connection, query=query)

    # HTML title in condor
    subquery = f"""
    (
        SELECT COALESCE({c.name}.{html_title}, '') AS title, {c.name}.{c.normalized_url.name}, ARRAY_AGG ({c.name}.{c.id.name}) AS condor_id
        FROM {c.name}
        GROUP BY ({c.name}.{html_title}, {c.name}.{c.normalized_url.name})
    )"""

    # Add condor ids for existing title-urls pairs in claim table
    query = f"""
    UPDATE {claim_table.name}
    SET title = c.title,
        normalized_url = c.{c.normalized_url.name},
        condor_id = ARRAY_CAT ({claim_table.name}.{claim_table.condor_ids.name}, c.condor_id)
    FROM {subquery} c
    WHERE ({claim_table.name}.{claim_table.title.name} = c.title
    AND {claim_table.name}.{claim_table.normalized_url.name} = c.{c.normalized_url.name})
    """
    execute_query(connection=connection, query=query)

    # Insert new title-url pairs from condor into claim table
    query = f"""
    INSERT INTO {claim_table.name}
    SELECT c.title, c.normalized_url, c.condor_id AS {claim_table.condor_ids.name}
    FROM {subquery} c
    JOIN {claim_table.name}
    ON {claim_table.name}.{claim_table.title.name} = c.title
    AND {claim_table.name}.{claim_table.normalized_url.name} = c.{c.normalized_url.name}
    WHERE {claim_table.name}.{claim_table.title.name} IS NULL
    AND {claim_table.name}.{claim_table.normalized_url.name} IS NULL
    """
    print(query)


def add_titles_to_data_sources(connection: psycopg2_connection):
    title_table = EnrichedURLTitleDataset()
    columns = [
        title_table.title_from_html.name,
        title_table.title_from_webarchive.name,
        title_table.title_from_youtube.name,
    ]

    def add_column(table_name, column_name):
        query = f"""
        ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} TEXT
        """
        execute_query(connection=connection, query=query)

    def update_table(table_name: str, column_name: str, url_id_col: str):
        query = f"""
        UPDATE {table_name}
            SET {column_name} = {title_table.name}.{column_name}
            FROM {title_table.name}
            WHERE {title_table.name}.{title_table.url_id.name} = {table_name}.{url_id_col}
        """
        execute_query(connection=connection, query=query)

    # Add enriched titles to De Facto
    table = DeFactoTable()
    print("Altering De Facto table to have enriched title columns")
    url_id_col = table.url_id.name
    for column_name in columns:
        add_column(table_name=table.name, column_name=column_name)
        update_table(
            table_name=table.name, column_name=column_name, url_id_col=url_id_col
        )

    # Add enriched titles to Science Feedback
    table = ScienceFeedbackTable()
    print("Altering Science Feedback table to have enriched title columns")
    url_id_col = table.url_id.name
    for column_name in columns:
        add_column(table_name=table.name, column_name=column_name)
        update_table(
            table_name=table.name, column_name=column_name, url_id_col=url_id_col
        )

    # Add enriched titles to Condor
    table = CondorTable()
    print("Altering Condor table to have enriched title columns")
    url_id_col = table.url_id.name
    for column_name in columns:
        add_column(table_name=table.name, column_name=column_name)
        update_table(
            table_name=table.name, column_name=column_name, url_id_col=url_id_col
        )
