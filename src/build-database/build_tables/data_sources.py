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
    URLTable,
)


def insert_data_sources(connection: psycopg2_connection):
    # From the imported completed_urls_dataset, build a table with a Condor ID from the condor table
    build_completed_urls_table(connection=connection)

    # Link the completed URLs table to the condor table
    completed_url_table = CompletedURLsTable()
    condor_table = CondorTable()
    completed_url_table.add_foreign_key(
        column=completed_url_table.condor_table_id.name,
        references=(condor_table.name, condor_table.id.name),
        connection=connection,
    )

    # From data source SQL tables, build URL table
    tables = [completed_url_table, condor_table, DeFactoTable(), ScienceFeedbackTable()]
    build_url_table(connection=connection, tables=tables)


def build_completed_urls_table(connection: psycopg2_connection):
    dataset_table = CompletedURLDatasetTable()
    completed_url_table = CompletedURLsTable()
    condor_table = CondorTable()

    # empty the target table
    completed_url_table.create(connection=connection)
    completed_url_table.drop(connection=connection)
    completed_url_table.create(connection=connection)

    condor = condor_table.name
    dataset = dataset_table.name

    # Selected columns from the join
    join_selection = f"""
    {dataset}.{dataset_table.url_id.name} AS {completed_url_table.url_id.name},
    {condor}.{condor_table.id.name} AS {completed_url_table.condor_table_id.name},
    {dataset}.{dataset_table.condor_url_rid.name} AS {completed_url_table.condor_url_rid.name},
    {dataset}.{dataset_table.completed_url.name} AS {completed_url_table.completed_url.name},
    {dataset}.{dataset_table.normalized_url.name} AS {completed_url_table.normalized_url.name},
    {dataset}.{dataset_table.original_url_id.name} AS {completed_url_table.original_url_id.name}
    """

    # Join on matched Condor URL RID and insert into table
    select_matches_on_condor_url_rid_id = f"""
    SELECT {join_selection} FROM {dataset} JOIN {condor}
    ON {dataset}.{dataset_table.condor_url_rid.name} = {condor}.{condor_table.condor_url_rid.name}
    AND {dataset}.{dataset_table.original_url_id.name} = {condor}.{condor_table.url_id.name}
    WHERE {dataset}.{dataset_table.condor_url_rid.name} IS NOT NULL
    """
    query = f"""
    INSERT INTO {completed_url_table.name} {select_matches_on_condor_url_rid_id}
    """
    execute_query(connection=connection, query=query)

    # Join on matched original URL ID without Condor URL RID and insert into table
    select_matches_on_url_id = f"""
    SELECT {join_selection} FROM {dataset} JOIN {condor}
    ON {dataset}.{dataset_table.original_url_id.name} = {condor}.{condor_table.url_id.name}
    WHERE {dataset}.{dataset_table.condor_url_rid.name} IS NULL
    """
    query = f"""
    INSERT INTO {completed_url_table.name} {select_matches_on_url_id}
    ON CONFLICT DO NOTHING
    """
    execute_query(connection=connection, query=query)


def build_url_table(connection: psycopg2_connection, tables: list[BaseTable]):
    url_table = URLTable()

    # empty the target table
    url_table.create(connection=connection)
    url_table.drop(connection=connection)
    url_table.create(connection=connection)

    def insert(table_name):
        query = f"""
        INSERT INTO {url_table.name}
        SELECT url_id AS id, normalized_url
        FROM {table_name}
        GROUP BY url_id, normalized_url
        ON CONFLICT (id) DO NOTHING
        """
        execute_query(connection=connection, query=query)

    def add_foreign_key(table_name):
        query = f"""
        ALTER TABLE {table_name} ADD FOREIGN KEY (url_id) REFERENCES {url_table.name} ({url_table.id.name})
        """
        execute_query(connection=connection, query=query)

    for table in tables:
        print(f"Inserting data from table {table.name} into {url_table.name}.")
        insert(table_name=table.name)
        add_foreign_key(table_name=table.name)
