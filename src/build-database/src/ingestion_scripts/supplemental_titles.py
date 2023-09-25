import csv

import casanova
from psycopg2.extensions import connection
from tqdm import tqdm

from table_schemas.supplemental_titles import SupplementalTitlesDatasetTable
from table_schemas.utils import basic_csv_row_cleaning, clear_table


def create_supplemental_titles_dataset_table(connection: connection, dataset: str):
    title_table = SupplementalTitlesDatasetTable()
    print(f"Creating table of supplemental titles in table {title_table.name}")
    clear_table(connection=connection, table=title_table)
    file_length = casanova.reader.count(dataset)
    with open(dataset) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            data = basic_csv_row_cleaning(row)
            title_table.insert_values(
                data=data,
                connection=connection,
                on_conflict="DO NOTHING",
            )
    return title_table
