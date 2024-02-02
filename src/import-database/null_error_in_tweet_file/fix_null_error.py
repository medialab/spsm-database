# Script to read error log for inserting values into Users table that have Null values

import ast
import csv
import re
from typing import Dict

import click

COLUMNS = (
    "id",
    "timestamp_utc",
    "location",
    "verified",
    "description",
    "url",
    "image",
    "tweets",
    "followers",
    "friends",
    "likes",
    "lists",
    "created_at",
    "collection_time",
    "display_name",
    "handle",
)


@click.command()
@click.argument("logfile")
@click.argument("outfile")
def user_null_error(logfile, outfile):
    with open(logfile) as f:
        log = f.readlines()

    values = [parse_values(l) for l in log if l.startswith("values: (")]

    with open(outfile, "w") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows([v for v in values if v])


def parse_values(values_string: str) -> Dict | None:
    values_string = values_string.strip()
    match = re.match(r"^values:\s\((.*)\)$", values_string)
    if match:
        value_match = match.group(1)
        value_list = ast.literal_eval(value_match)
        return dict(zip(COLUMNS, value_list))


if __name__ == "__main__":
    user_null_error()
