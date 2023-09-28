import csv

import casanova
from tqdm import tqdm

from table_schemas.title_query import TitleQueryDatasetTable
from table_schemas.utils import clear_table


def clean(data: dict) -> dict:
    """Script for parsing and cleaning CSV file rows."""
    for k, v in data.items():
        if v == "":
            v = None
        elif isinstance(v, str):
            v = v.strip()
        if k == "manually_skipped" or k == "same_as_original" or k == "concatenation":
            if v == "0":
                v = False
            else:
                v = True
        data.update({k: v})
    return data


def insert(connection, dataset):
    table = TitleQueryDatasetTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data to table: {table.name}\n{dataset}")

    # Ingest all of the dataset into the Searchable Titles & URLS table
    file_length = casanova.reader.count(dataset)
    with open(dataset) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            table.insert_values(
                data=clean(data=row),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    return table
