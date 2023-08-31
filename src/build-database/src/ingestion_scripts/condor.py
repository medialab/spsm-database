import csv

import casanova
from tqdm import tqdm

from table_schemas.condor import CondorDatasetTable
from table_schemas.enriched_titles import (
    add_enriched_titles,
    setup_enriched_title_dataset_table,
)
from table_schemas.utils import clear_table


def clean(data: dict) -> dict:
    """Script for parsing and cleaning Condor CSV file rows."""
    condor_id = data.pop("url_rid")
    url_id = data.pop("hash")
    normalized_url = data.pop("normalized_url")
    data.update(
        {
            "condor_url_rid": condor_id,
            "normalized_clean_url_hash": url_id,
            "normalized_clean_url": normalized_url,
        }
    )

    tpfc_rating = data.get("tpfc_rating")
    CONDOR_RATINGS = {
        "fact checked as false": 1.0,
        "fact checked as altered media": 2.0,
        "fact checked as missing context": 3.0,
        "fact checked as mixture or false headline": 3.0,
        "opinion": 4.0,
        "fact checked as true": 5.0,
    }
    data.update({"normalized_fact_check_rating": None})
    if tpfc_rating and tpfc_rating in CONDOR_RATINGS.keys():
        data.update({"normalized_fact_check_rating": CONDOR_RATINGS[tpfc_rating]})

    for k, v in data.items():
        if v == "":
            v = None
        elif isinstance(v, str):
            v = v.strip()
        data.update({k: v})
    return data


def insert(connection, dataset, supplemental_titles):
    # Prepare Condor table for new data ingestion
    table = CondorDatasetTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data to table: {table.name}\n{dataset}")

    # Ingest all of the dataset into the Condor table
    file_length = casanova.reader.count(dataset)
    with open(dataset) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            table.insert_values(
                data=clean(data=row),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    # Enrich the Condor dataset table with titles
    setup_enriched_title_dataset_table(
        connection=connection, dataset=supplemental_titles
    )
    print(f"\nAltering the table {table.name} to have columns for enriched titles.")
    add_enriched_titles(
        connection=connection,
        target_url_id_col_name="normalized_clean_url_hash",
        target_table=table,
    )

    return table
