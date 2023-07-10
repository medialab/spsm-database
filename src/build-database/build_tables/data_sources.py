# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for inserting original data sources into SQL tables
#
from psycopg2.extensions import connection as psycopg2_connection

from connection.execute_query import execute_query
from tables.schemas import (
    ClaimTitleTable,
    CompletedURLTable,
    CondorTable,
    DeFactoTable,
    EnrichedURLTitleDataset,
    ScienceFeedbackTable,
)
from utils import clear_table


def insert_data_sources(connection: psycopg2_connection):
    # Associate completed URLs from dataset with entities in the Condor dataset table
    print("\n=========================================\nBuilding Completed URL table.")
    build_completed_urls_table(connection=connection)

    # Add enriched titles to each entity in the 3 data source tables
    print(
        "\n=========================================\nAdding enriched titles to claims in data sources."
    )
    add_titles_to_data_sources(connection=connection)

    # Relate every title to a claim ID
    print("\n=========================================\nRelating claims to titles.")
    create_claim_title_relations(connection=connection)


def create_claim_title_relations(connection: psycopg2_connection):
    # Set up relational table
    table = ClaimTitleTable()
    clear_table(connection=connection, table=table)

    # If a claim has a title, add its ID, title, and title type
    # to the relational table
    titles_dataset = EnrichedURLTitleDataset()
    html_title = titles_dataset.title_from_html.name
    youtube_title = titles_dataset.title_from_youtube.name
    archive_title = titles_dataset.title_from_webarchive.name

    # Get tables
    condor = CondorTable()
    defacto = DeFactoTable()
    science = ScienceFeedbackTable()
    tables = [
        (table.condor_id.name, condor),
        (table.science_id.name, science),
        (table.defacto_id.name, defacto),
    ]

    # Add Condor share title
    share_title = condor.share_title.name
    condor_table = condor.name
    print(f"\nAdding Condor share title to relational table '{table.name}'.")
    query = f"""
    INSERT INTO {table.name}({table.title.name}, {table.title_type.name}, {table.condor_id.name})
    SELECT {share_title}, 'condor_share_title', {condor.id.name}
    FROM {condor_table}
    WHERE {share_title} IS NOT NULL
    """
    execute_query(connection=connection, query=query)

    # Add HTML title
    print(f"\nAdding scraped HTML titles to relational table '{table.name}'.")
    for id_col, source_table in tables:
        query = f"""
        INSERT INTO {table.name}({table.title.name}, {table.title_type.name}, {id_col})
        SELECT {html_title}, 'html', {source_table.id.name}
        FROM {source_table.name}
        WHERE {html_title} IS NOT NULL
        """
        execute_query(connection=connection, query=query)

    # Add YouTube title
    print(f"\nAdding YouTube video titles to relational table '{table.name}'.")
    for id_col, source_table in tables:
        query = f"""
        INSERT INTO {table.name}({table.title.name}, {table.title_type.name}, {id_col})
        SELECT {youtube_title}, 'youtube', {source_table.id.name}
        FROM {source_table.name}
        WHERE {youtube_title} IS NOT NULL
        """
        execute_query(connection=connection, query=query)

    # Add Web Archive title
    print(f"\nAdding Web Archive video titles to relational table '{table.name}'.")
    for id_col, source_table in tables:
        query = f"""
        INSERT INTO {table.name}({table.title.name}, {table.title_type.name}, {id_col})
        SELECT {archive_title}, 'youtube', {source_table.id.name}
        FROM {source_table.name}
        WHERE {archive_title} IS NOT NULL
        """
        execute_query(connection=connection, query=query)

    # Relate Condor titles to Condor table
    table.add_foreign_key(
        column=table.condor_id.name,
        references=(condor.name, condor.id.name),
        connection=connection,
    )

    # Relate De Facto titles to De Facto table
    table.add_foreign_key(
        column=table.defacto_id.name,
        references=(defacto.name, defacto.id.name),
        connection=connection,
    )

    # Relate Science Feedback titles to Science Feedback table
    table.add_foreign_key(
        column=table.science_id.name,
        references=(science.name, science.id.name),
        connection=connection,
    )


def build_completed_urls_table(connection: psycopg2_connection):
    completed_url_table = CompletedURLTable()
    condor_table = CondorTable()

    # Get column names from the Condor table
    condor = condor_table.name
    condor_table_id = condor_table.id.name
    condor_url_hash = condor_table.normalized_clean_url_hash.name
    condor_url_rid = condor_table.condor_url_rid.name

    # Get column names from the Completed URLs table
    dataset = completed_url_table.name
    dataset_condor_table_id = completed_url_table.condor_table_id.name
    dataset_condor_url_rid = completed_url_table.condor_url_rid.name
    dataset_original_url_hash = completed_url_table.hash_of_original_normalized_url.name

    task = """
If they have a corresponding Condor URL RID in the Condor table,
update the completed URLs' Condor table ID foreign key by
matching on the original URL hash and the Condor URL RID.
    """
    query = f"""
    UPDATE {dataset}
    SET {dataset_condor_table_id} = s.{condor_table_id}
    FROM (
        SELECT  {dataset}.{dataset_condor_url_rid},
                {dataset}.{dataset_original_url_hash},
                {condor}.{condor_table_id}
        FROM {dataset}
        INNER JOIN {condor}
        ON {dataset}.{dataset_original_url_hash} = {condor}.{condor_url_hash}
        AND {dataset}.{dataset_condor_url_rid} = {condor}.{condor_url_rid}
        ) s
    WHERE s.{dataset_condor_url_rid} IS NOT NULL
    AND {dataset}.{dataset_original_url_hash} = s.{dataset_original_url_hash}
    AND {dataset}.{dataset_condor_url_rid} = s.{dataset_condor_url_rid}
    """
    print(task, query)
    execute_query(connection=connection, query=query)

    task = """
If they don't have a corresponding Condor URL RID in the Condor table,
update the completed URLs' Condor table ID foreign key by matching
on the original URL hash and the lack of a Condor URL RID.
    """
    query = f"""
    UPDATE {dataset}
    SET {dataset_condor_table_id} = s.{condor_table_id}
    FROM (
        SELECT  {dataset}.{dataset_condor_url_rid},
                {dataset}.{dataset_original_url_hash},
                {condor}.{condor_table_id}
        FROM {dataset}
        INNER JOIN {condor}
        ON {dataset}.{dataset_original_url_hash} = {condor}.{condor_url_hash}
        ) s
    WHERE s.{dataset_condor_url_rid} IS NULL
    AND {dataset}.{dataset_original_url_hash} = s.{dataset_original_url_hash}
    """
    print(task, query)
    execute_query(connection=connection, query=query)

    # Add a foreign key relating the Condor table's ID with
    # the enriched / "completed" URL in the completed URL table
    completed_url_table.add_foreign_key(
        column=completed_url_table.condor_table_id.name,
        references=(condor_table.name, condor_table.id.name),
        connection=connection,
    )


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
    print("\nAltering De Facto table to have enriched title columns")
    url_id_col = table.url_id.name
    for column_name in columns:
        add_column(table_name=table.name, column_name=column_name)
        update_table(
            table_name=table.name, column_name=column_name, url_id_col=url_id_col
        )

    # Add enriched titles to Science Feedback
    table = ScienceFeedbackTable()
    print("\nAltering Science Feedback table to have enriched title columns")
    url_id_col = table.url_id.name
    for column_name in columns:
        add_column(table_name=table.name, column_name=column_name)
        update_table(
            table_name=table.name, column_name=column_name, url_id_col=url_id_col
        )

    # Add enriched titles to Condor
    table = CondorTable()
    print("\nAltering Condor table to have enriched title columns")
    url_id_col = table.normalized_clean_url_hash.name
    for column_name in columns:
        add_column(table_name=table.name, column_name=column_name)
        update_table(
            table_name=table.name, column_name=column_name, url_id_col=url_id_col
        )
