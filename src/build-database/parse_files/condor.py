import csv

import casanova
from tqdm import tqdm

from tables.schemas import CondorTable
from utils import clear_table


def clean(data: dict) -> dict:
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
    for k, v in data.items():
        if v == "":
            v = None
        elif isinstance(v, str):
            v = v.strip()
        data.update({k: v})
    return data


def insert(connection, file):
    condor_table = CondorTable()
    clear_table(connection=connection, table=condor_table)
    print(f"\nImporting data from Condor to table: {condor_table.name}\n{file}")
    file_length = casanova.reader.count(file)
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            condor_table.insert_values(
                data=clean(data=row),
                connection=connection,
                on_conflict="DO NOTHING",
            )
