import csv
import json
import os
from datetime import datetime

import click
from elasticsearch import Elasticsearch
from tqdm.auto import tqdm


@click.command()
@click.option("-f", "--filename", required=True, help="CSV file to be indexed.")
@click.option("-i", "--indexname", required=True, help="Name of the index to be created/udpated.")
@click.option("-m", "--mapping", required=True, help="JSON mapping of CSV columns to index.")
@click.option("-k", "--key", required=True, help="Unique ID for each entry in the index.")
def main(filename, indexname, mapping, key):

    # ----------------------------------------------------#
    # CONFIRM DATA SOURCE

    if not os.path.isfile(filename):
        raise FileNotFoundError(f"\n    The data file was not found. The path given was: {filename}")
    else:
        DATA = filename

    # ----------------------------------------------------#
    # CONFIGURATION FOR ELASTIC SEARCH CLIENT

    PERSONAL_CONFIG = "config.json"

    if os.path.isfile(PERSONAL_CONFIG):
        config = PERSONAL_CONFIG
    else:
        raise FileNotFoundError("Configuration file not found.")

    with open(config, "r") as f:
        config = json.load(f)["elastic-search"]
        ELASTIC_PASSWORD = config.get("ELASTIC_PASS")
        ELASTIC_USER = config.get("ELASTIC_USER")
        CERT_FINGERPRINT = config.get("ELASTIC_CERT_FINGERPRINT")
        ELASTIC_HOST = config["ELASTIC_HOST"]

    # ----------------------------------------------------#
    # CREATE CLIENT
    if ELASTIC_PASSWORD:
        client = Elasticsearch(
            ELASTIC_HOST,
            ssl_assert_fingerprint=CERT_FINGERPRINT,
            basic_auth=(ELASTIC_USER, ELASTIC_PASSWORD)
            )
    else:
        client = Elasticsearch(ELASTIC_HOST)

    # ----------------------------------------------------#
    # CREATE INDEX WITH MAPPING
    with open(mapping, "r") as f:
        mapping = json.load(f)

    if not client.indices.exists(index=indexname):
        client.indices.create(index=indexname, **mapping)

    # ----------------------------------------------------#
    # ADD DOCUMENTS
    with open(DATA, "r") as f:
        csv_reader = csv.DictReader(f)

        for row in csv_reader: pass
        total = csv_reader.line_num
        f.seek(0)
        next(csv_reader)

        for row in tqdm(csv_reader, total=total, desc="Progress Bar", dynamic_ncols=True):
            if "date" in row.keys() and not row["date"]:
                row.update({"date":"1900-01-01 00:00:00"})

            if "archive_timestamp" in row.keys() and not row["archive_timestamp"]:
                row.update({"archive_timestamp":"1900-01-01 00:00:00"})

            client.index(index=indexname, id=row.pop(key), document=row)


if __name__ == "__main__":
    main()