import csv

import casanova
from tqdm import tqdm

from tables.schemas import TitlesTable, ClaimTitleTable
from utils import clear_table


def clean(data: dict) -> dict:
    skip = data.pop("queried")
    queried = False
    if skip == "0":
        queried = True
    return {
        "title_text": data["title_text"].strip(),
        "tweet_search_title": data["tweet_search_title"],
        "queried": queried,
    }


def insert(connection, file):
    table = TitlesTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data from Dataset to table: {table.name}\n{file}")
    file_length = casanova.reader.count(file)
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            table.insert_values(
                data=clean(data=row), connection=connection, on_conflict="DO NOTHING"
            )
    rel_table = ClaimTitleTable()
    rel_table.add_foreign_key(
        column=rel_table.title.name,
        references=(table.name, table.title.name),
        connection=connection,
    )
