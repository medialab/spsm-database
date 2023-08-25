from psycopg2.extensions import connection as psycopg2_connection

from table_schemas.claims import ClaimsTable
from table_schemas.doc_title_relation import DocTitleRelationTable
from table_schemas.utils import clear_table, BaseTable
from utils import execute_query


def create_doc_title_relation_table(connection: psycopg2_connection) -> BaseTable:
    claims_table = ClaimsTable()

    doc_title_relation_table = DocTitleRelationTable()
    clear_table(connection=connection, table=doc_title_relation_table)

    query = f"""
insert into {doc_title_relation_table.name} (claim_id, normalized_url, title_text, title_type)
SELECT id AS claim_id, normalized_url, title_from_html AS title_text, 'html' AS title_type FROM {claims_table.name}
UNION ALL
SELECT id AS claim_id, normalized_url, title_from_condor AS title_text, 'condor' AS title_type FROM {claims_table.name}
UNION ALL
SELECT id AS claim_id, normalized_url, title_from_youtube AS title_text, 'youtube' AS title_type FROM {claims_table.name}
UNION ALL
SELECT id AS claim_id, normalized_url, title_from_web_archive AS title_text, 'web_archive' AS title_type FROM {claims_table.name}
    """
    print("\nBuilding table for relations between a document (URL) and a title.")
    execute_query(connection=connection, query=query)
    doc_title_relation_table.add_foreign_key(
        foreign_key_column="claim_id",
        target_table=claims_table.name,
        target_table_primary_key=claims_table.pk,
        connection=connection,
    )

    return doc_title_relation_table
