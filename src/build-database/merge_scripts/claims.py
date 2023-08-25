from psycopg2.extensions import connection as psycopg2_connection

from merge_scripts.insert_claims import insert_data
from merge_scripts.utils import Mapper
from table_schemas.claims import ClaimsTable
from table_schemas.completed_urls import CompletedURLDatasetTable
from table_schemas.condor import CondorDatasetTable
from table_schemas.de_facto import DeFactoDatasetTable
from table_schemas.science import ScienceFeedbackDatasetTable
from table_schemas.utils import clear_table


def create_claims_table(connection: psycopg2_connection):
    claims_table = ClaimsTable()
    clear_table(connection=connection, table=claims_table)

    # Merge Condor data
    c = Mapper(
        source_table_name=CondorDatasetTable().name,
        source_table_primary_key=CondorDatasetTable().pk,
        source_table_id="condor_table_id",
        source_normalized_url="normalized_clean_url",
        source_normalized_url_hash="normalized_clean_url_hash",
    )
    print(f"\nMerging data from {c.source_table_name} into {claims_table.name}")
    insert_data(connection=connection, data=c)
    claims_table.add_foreign_key(
        foreign_key_column=c.source_table_id,
        target_table=c.source_table_name,
        target_table_primary_key=c.source_table_primary_key,
        connection=connection,
    )

    # Merge De Facto data
    d = Mapper(
        source_table_name=DeFactoDatasetTable().name,
        source_table_primary_key=DeFactoDatasetTable().pk,
        source_table_id="de_facto_table_id",
        source_normalized_url="normalized_claim_url",
        source_normalized_url_hash="normalized_claim_url_hash",
    )
    print(f"\nMerging data from {d.source_table_name} into {claims_table.name}")
    insert_data(connection=connection, data=d)
    claims_table.add_foreign_key(
        foreign_key_column=d.source_table_id,
        target_table=d.source_table_name,
        target_table_primary_key=d.source_table_primary_key,
        connection=connection,
    )

    # Merge Science Feedback data
    s = Mapper(
        source_table_name=ScienceFeedbackDatasetTable().name,
        source_table_primary_key=ScienceFeedbackDatasetTable().pk,
        source_table_id="science_feedback_table_id",
        source_normalized_url="normalized_claim_url",
        source_normalized_url_hash="normalized_claim_url_hash",
    )
    print(f"\nMerging data from {s.source_table_name} into {claims_table.name}")
    insert_data(connection=connection, data=s)
    claims_table.add_foreign_key(
        foreign_key_column=s.source_table_id,
        target_table=s.source_table_name,
        target_table_primary_key=s.source_table_primary_key,
        connection=connection,
    )

    # Merge completed URLs
    u = Mapper(
        source_table_name=CompletedURLDatasetTable().name,
        source_table_primary_key=CompletedURLDatasetTable().pk,
        source_table_id="completed_url_table_id",
        source_normalized_url="completed_normalized_url",
        source_normalized_url_hash="completed_normalized_url_hash",
    )
    print(f"\nMerging data from {u.source_table_name} into {claims_table.name}")
    insert_data(connection=connection, data=s, normalized_url_only=True)
    claims_table.add_foreign_key(
        foreign_key_column=u.source_table_id,
        target_table=u.source_table_name,
        target_table_primary_key=u.source_table_primary_key,
        connection=connection,
    )
