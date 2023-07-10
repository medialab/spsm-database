import csv

import casanova
from minet.utils import md5
from tqdm import tqdm
from ural import normalize_url

from tables.schemas import CompletedURLTable
from utils import clear_table


def clean(data: dict) -> dict:
    original_url_id = data.pop("url_id")
    completed_url = data.pop("completed_normalized_url")
    normalized_url = normalize_url(completed_url)
    url_id = md5(normalized_url)
    d = {
        "completed_url": completed_url,
        "normalized_completed_url": normalized_url,
        "completed_url_hash": url_id,
        "hash_of_original_normalized_url": original_url_id,
        "condor_url_rid": data["condor_id"],
    }
    for k, v in d.items():
        if v == "":
            v = None
        d.update({k: v})
    return d


def insert(connection, file):
    table = CompletedURLTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data from Completed URLs to table: {table.name}\n{file}")
    file_length = casanova.reader.count(file)
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            table.insert_values(
                data=clean(row),
                connection=connection,
                on_conflict="DO NOTHING",
            )
