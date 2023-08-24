import csv

import casanova
from minet.utils import md5
from tqdm import tqdm

from table_schemas.completed_urls import CompletedURLDatasetTable
from table_schemas.condor import CondorDatasetTable
from table_schemas.utils import clear_table
from utils import execute_query


def clean(data: dict) -> dict:
    completed_url = data.get("completed_normalized_url")
    url_id = md5(completed_url)
    d = {
        "completed_normalized_url_hash": url_id,
        "completed_normalized_url": completed_url,
        "hash_of_original_normalized_url": data["url_id"],
        "condor_url_rid": data["condor_id"],
    }
    for k, v in d.items():
        if v == "":
            v = None
        d.update({k: v})
    return d


def insert(connection, file):
    table = CompletedURLDatasetTable()
    clear_table(connection=connection, table=table)
    print(
        f"\nImporting data from Completed URLs dataset to table: {table.name}\n{file}"
    )
    file_length = casanova.reader.count(file)
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            table.insert_values(
                data=clean(row),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    link_to_condor_table(connection=connection)
    return table


def link_to_condor_table(connection):
    completed_url_table = CompletedURLDatasetTable()
    condor_table = CondorDatasetTable()

    task = """
If a completed URL has a Condor URL RID, update its Condor
table ID foreign key by joining on the original URL hash as
well as the Condor URL RID.
    """
    query = f"""
    UPDATE {completed_url_table.name}
    SET condor_table_id = s.id
    FROM (
        SELECT  {completed_url_table.name}.condor_url_rid,
                {completed_url_table.name}.hash_of_original_normalized_url,
                {condor_table.name}.id
        FROM {completed_url_table.name}
        INNER JOIN {condor_table.name}
        ON {completed_url_table.name}.hash_of_original_normalized_url = {condor_table.name}.normalized_clean_url_hash
        AND {completed_url_table.name}.condor_url_rid = {condor_table.name}.condor_url_rid
        ) s
    WHERE s.condor_url_rid IS NOT NULL
    AND {completed_url_table.name}.hash_of_original_normalized_url = s.hash_of_original_normalized_url
    AND {completed_url_table.name}.condor_url_rid = s.condor_url_rid
    """
    print(task, query)
    execute_query(connection=connection, query=query)

    task = """
If a completed URL does not have a Condor URL RID, update its
Condor table ID by joining on the original URL hash as well as
the lack of a Condor URL RID.
    """
    query = f"""
    UPDATE {completed_url_table.name}
    SET condor_table_id = s.id
    FROM (
        SELECT  {completed_url_table.name}.condor_url_rid,
                {completed_url_table.name}.hash_of_original_normalized_url,
                {condor_table.name}.id
        FROM {completed_url_table.name}
        INNER JOIN {condor_table.name}
        ON {completed_url_table.name}.hash_of_original_normalized_url = {condor_table.name}.normalized_clean_url_hash
        ) s
    WHERE s.condor_url_rid IS NULL
    AND {completed_url_table.name}.hash_of_original_normalized_url = s.hash_of_original_normalized_url
    """
    print(task, query)
    execute_query(connection=connection, query=query)

    # Add a foreign key relating the Condor table's ID with
    # the enriched / "completed" URL in the completed URL table
    completed_url_table.add_foreign_key(
        column="condor_table_id",
        references=(condor_table.name, "id"),
        connection=connection,
    )
