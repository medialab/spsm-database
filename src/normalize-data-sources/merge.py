import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import casanova
from CONSTANTS import CONDOR_FIELDS, DEFACTO_FIELDS, SCIENCE_FIELDS
from tqdm.auto import tqdm

today = str(datetime.today().date())


def file_exists(input):
    path = Path(input)
    if path.is_file():
        return path
    else:
        raise FileNotFoundError(input)


@dataclass
class SharedFields:
    merged_date_format = "%Y-%m-%d %H:%M:%S"
    fields = [
        "url_id",
        "date",
        "sources",
        "normalized_url",
        "archive_url",
        "archive_timestamp",
    ]

    @dataclass
    class Condor:
        url_column = "clean_url"
        id_column = "url_rid"
        date_column = "first_post_time"
        date_format = "%Y-%m-%d %H:%M:%S.%f"

    @dataclass
    class DeFacto:
        url_column = "claim-review_itemReviewed_appearance_url"
        id_column = "id"
        date_column = "claim-review_itemReviewed_datePublished"
        date_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    @dataclass
    class Science:
        url_column = "url"
        id_column = "id"
        date_column = "publishedDate"
        date_format = "%Y-%m-%dT%H:%M:%S%z"


class RowFormatter:
    def __init__(self, prefix: str) -> None:
        self.fields = getattr(SharedFields, prefix)
        self.prefix = prefix.lower()

    def row(self, row: dict) -> dict:
        date_column = getattr(self.fields, "date_column")
        date = row[date_column]
        if date:
            original_date_format = datetime.strptime(
                date, getattr(self.fields, "date_format")
            )
            standard_date_format = datetime.strptime(
                original_date_format.strftime(SharedFields.merged_date_format),
                SharedFields.merged_date_format,
            )
            row["date"] = standard_date_format
        else:
            row["date"] = None
        url_column = getattr(self.fields, "url_column")
        row["archive_url"] = row[url_column]
        row["sources"] = self.prefix
        row["url_id"] = row["hash"]
        row.pop("hash")
        return row

    def rename_fields(self, row: dict) -> dict:
        renamed_row = {}
        for k, v in row.items():
            if k not in SharedFields.fields:
                k = "{}_{}".format(self.prefix, k)
            renamed_row[k] = v
        return renamed_row


def main():
    # ------------------------------------------------------- #
    # 0. Parse the Command-Line arguments
    parser = argparse.ArgumentParser(
        prog="Merge",
        description="Merge 3 flattened data source CSV files.",
    )
    parser.add_argument("--condor", type=file_exists)
    parser.add_argument("--defacto", type=file_exists)
    parser.add_argument("--science", type=file_exists)
    parser.add_argument("output_dir", type=str)
    args = parser.parse_args()
    condor_filepath, defacto_filepath, sf_filepath, output_dir = (
        args.condor,
        args.defacto,
        args.science,
        args.output_dir,
    )
    if not Path(output_dir).is_dir():
        raise NotADirectoryError
    merged_filepath = Path(output_dir).joinpath(f"aggregated_{today}.csv")
    concatenated_filepath = Path(output_dir).joinpath(f"concatenated_{today}.csv")

    # ------------------------------------------------------- #
    # 1. Establish the merged file's fieldnames
    fieldnames_with_prefix = []
    for name in DEFACTO_FIELDS:
        if name not in SharedFields.fields:
            name = "{}_{}".format("defacto", name)
        fieldnames_with_prefix.append(name)
    for name in CONDOR_FIELDS:
        if name not in SharedFields.fields:
            name = "{}_{}".format("condor", name)
        fieldnames_with_prefix.append(name)
    for name in SCIENCE_FIELDS:
        if name not in SharedFields.fields:
            name = "{}_{}".format("science", name)
        fieldnames_with_prefix.append(name)
    fieldnames_with_prefix = sorted(list(set(fieldnames_with_prefix)))
    merge_field_names = SharedFields.fields + fieldnames_with_prefix

    # ------------------------------------------------------- #
    # 2. Store all URL IDs in an index
    url_id_index = {}

    # ------------------------------------------------------- #
    # 3. Index all the Condor data by the URL ID
    print("\nFormatting Condor data.")
    total = casanova.reader.count(condor_filepath)
    formatter = RowFormatter("Condor")
    with open(condor_filepath) as f, open(concatenated_filepath, "a") as of:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(of, fieldnames=merge_field_names)
        writer.writeheader()
        for row in tqdm(reader, total=total):
            # Format the data's date and add universal columns
            row_with_formatted_date = formatter.row(row)
            # Rename certain columns with the dataset's prefix
            row_with_renamed_fields = formatter.rename_fields(row_with_formatted_date)
            # Append this data to the URL Index
            url_id = row_with_renamed_fields["url_id"]
            if not url_id_index.get(url_id):
                url_id_index[url_id] = []
            url_id_index[url_id].append(row_with_renamed_fields)
            writer.writerow(row_with_renamed_fields)

    # ------------------------------------------------------- #
    # 4. Index all the De Facto data by the URL ID
    print("\nFormatting De Facto data.")
    total = casanova.reader.count(defacto_filepath)
    formatter = RowFormatter("DeFacto")
    with open(defacto_filepath) as f, open(concatenated_filepath, "a") as of:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(of, fieldnames=merge_field_names)
        writer.writeheader()
        for row in tqdm(reader, total=total):
            # Format the data's date and add universal columns
            row_with_formatted_date = formatter.row(row)
            # Rename certain columns with the dataset's prefix
            row_with_renamed_fields = formatter.rename_fields(row_with_formatted_date)
            # Append this data to the URL Index
            url_id = row_with_renamed_fields["url_id"]
            if not url_id_index.get(url_id):
                url_id_index[url_id] = []
            url_id_index[url_id].append(row_with_renamed_fields)
            writer.writerow(row_with_renamed_fields)

    # ------------------------------------------------------- #
    # 5. Index all the Science Feedback data by the URL ID
    print("\nFormatting Science Feeback data.")
    total = casanova.reader.count(sf_filepath)
    formatter = RowFormatter("Science")
    with open(sf_filepath) as f, open(concatenated_filepath, "a") as of:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(of, fieldnames=merge_field_names)
        writer.writeheader()
        for row in tqdm(reader, total=total):
            # Format the data's date and add universal columns
            row_with_formatted_date = formatter.row(row)
            # Rename certain columns with the dataset's prefix
            row_with_renamed_fields = formatter.rename_fields(row_with_formatted_date)
            # Append this data to the URL Index
            url_id = row_with_renamed_fields["url_id"]
            if not url_id_index.get(url_id):
                url_id_index[url_id] = []
            url_id_index[url_id].append(row_with_renamed_fields)
            writer.writerow(row_with_renamed_fields)

    # ------------------------------------------------------- #
    # 6. In one CSV file, merge all the data in the URL ID index
    print("\nAggregating by URL.")
    with open(merged_filepath, "w") as of:
        writer = csv.DictWriter(of, fieldnames=merge_field_names)
        writer.writeheader()
        for url_id, data in tqdm(url_id_index.items(), total=len(url_id_index)):
            # 6.a Establish an empty version of the merged row
            merged_row = {k: None for k in merge_field_names}
            # 6.b In case a dataset has duplicate URLs, concatenate the dataset's metadata
            for row in data:
                for k, v in row.items():
                    if k not in SharedFields.fields:
                        if merged_row[k]:
                            concatenation = [merged_row[k], v]
                            v = "|".join(concatenation)
                    merged_row[k] = v
            # 6.c For the row's "date" column, get the oldest date for this URL
            dates = sorted([row["date"] for row in data if row["date"]])
            if len(dates) > 0:
                oldest_date = dates[0]
            else:
                oldest_date = None
            merged_row["date"] = oldest_date
            # 6.d For the row's "source" column, get a list of unique sources
            sources = sorted(list(set([row["sources"] for row in data])))
            if len(sources) > 1:
                sources = "|".join(sources)
            merged_row["sources"] = sources
            writer.writerow(merged_row)


if __name__ == "__main__":
    main()
