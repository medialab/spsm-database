from minet.utils import md5
from ural import normalize_url
from tables.schemas import CompletedURLDatasetTable
import casanova
import csv
from tqdm import tqdm


def clean(data: dict) -> dict:
    original_url_id = data.pop("url_id")
    completed_url = data.pop("completed_normalized_url")
    normalized_url = normalize_url(completed_url)
    url_id = md5(normalized_url)
    d = {
        "completed_url": completed_url,
        "normalized_url": normalized_url,
        "url_id": url_id,
        "original_url_id": original_url_id,
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


def clear_table(connection, table):
    table.create(connection=connection)
    table.drop(connection=connection)
    table.create(connection=connection)