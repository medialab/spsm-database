import casanova
import csv

from tqdm import tqdm

from table_schemas.science import ScienceFeedbackDatasetTable
from table_schemas.utils import clear_table


def clean(data: dict) -> dict:
    clean_data = {}
    for k, v in data.items():
        if v == "":
            v = None
        elif isinstance(v, str):
            v = v.strip()
        clean_data.update({k: v})

    return clean_data


def insert(connection, dataset):
    table = ScienceFeedbackDatasetTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data to table: {table.name}\n{dataset}")
    file_length = casanova.reader.count(dataset)
    with open(dataset) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            table.insert_values(
                data=clean(row),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    return table
