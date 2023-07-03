# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for inserting original data sources into SQL tables
#
from connection.execute_query import execute_query
from psycopg2.extensions import connection as psycopg2_connection
from tables.schemas import (
    BaseTable,
    CompletedURLDatasetTable,
    CompletedURLsTable,
    CondorTable,
    DeFactoTable,
    ScienceFeedbackTable,
    EnrichedURLTitleDataset,
)


def insert_data_sources(connection: psycopg2_connection):
    # Add enriched titles to each item in the data source tables
    add_titles_to_data_sources(connection=connection)


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
