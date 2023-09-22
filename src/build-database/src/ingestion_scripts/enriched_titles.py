import csv

import casanova
from psycopg2.extensions import connection
from tqdm import tqdm

from table_schemas.enriched_titles import EnrichedTitleDatasetTable
from table_schemas.utils import basic_csv_row_cleaning, clear_table


def setup_enriched_title_dataset_table(connection: connection, dataset: str):
    title_table = EnrichedTitleDatasetTable()
    print(f"Creating table of enriched titles in table {title_table.name}")
    clear_table(connection=connection, table=title_table)
    file_length = casanova.reader.count(dataset)
    with open(dataset) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            row.pop("sources")
            data = basic_csv_row_cleaning(row)
            title_table.insert_values(
                data=data,
                connection=connection,
                on_conflict="DO NOTHING",
            )
    return title_table
