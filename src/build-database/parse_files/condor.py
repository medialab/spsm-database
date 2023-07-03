import csv

import casanova
from tqdm import tqdm

from tables.schemas import CondorTable
from utils import clear_table


def clean(data: dict) -> dict:
    condor_id = data.pop("url_rid")
    url_id = data.pop("hash")
    data.update({"condor_url_rid": condor_id, "url_id": url_id})
    for k, v in data.items():
        if v == "":
            data.update({k: None})
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
