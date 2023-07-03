import casanova
from tables.schemas import EnrichedURLTitleDataset
import csv
from tqdm import tqdm


def clean(data: dict) -> dict:
    for k, v in data.items():
        if v == "":
            data.update({k: None})
    return {
        "url_id": data["url_id"],
        "normalized_url": data["normalized_url"],
        "archive_url": data["archive_url"],
        "title_from_youtube": data["yt_video_headline"],
        "title_from_html": data["webpage_title"],
        "title_from_webarchive": data["webarchive_search_title"],
    }


def insert(connection, file):
    table = EnrichedURLTitleDataset()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data from Dataset to table: {table.name}\n{file}")
    file_length = casanova.reader.count(file)
    with open(file) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            table.insert_values(
                data=clean(data=row), connection=connection, on_conflict="DO NOTHING"
            )


def clear_table(connection, table):
    table.create(connection=connection)
    table.drop(connection=connection)
    table.create(connection=connection)
