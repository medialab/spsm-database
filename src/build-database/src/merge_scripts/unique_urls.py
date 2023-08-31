from psycopg2.extensions import connection as psycopg2_connection

from table_schemas.claims import ClaimsTable
from table_schemas.url_enrichments import URLEnrichmentsTable
from table_schemas.utils import clear_table, BaseTable
from utils import execute_query


def create_url_enrichment_table(connection: psycopg2_connection) -> BaseTable:
    claims_table = ClaimsTable()

    table = URLEnrichmentsTable()
    clear_table(connection=connection, table=table)

    query = f"""
INSERT INTO {table.name} (id)
SELECT DISTINCT(normalized_url_hash)
FROM {claims_table.name}
ON CONFLICT DO NOTHING
    """
    print("\nBuilding table to store extra metadata about URLs.")
    execute_query(connection=connection, query=query)

    # Add foreign key on claims table that links claims to
    # enrichments table via the normalized URL hash
    claims_table.add_foreign_key(
        foreign_key_column="normalized_url_hash",
        target_table=table.name,
        target_table_primary_key=table.pk,
        connection=connection,
    )

    return table
