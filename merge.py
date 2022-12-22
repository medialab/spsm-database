import csv
from datetime import datetime
import os

import click
from tqdm.auto import tqdm

from condor import CONDOR_FIELDS
from defacto import DEFACTO_FIELDS
from science import SCIENCE_FIELDS
from utils import FileNaming

SHARED_FIELDS = ["url_id", "date", "sources", "normalized_url", "archive_url", "archive_timestamp"]


class Fields():

    merged_date_format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, dataset):
        if dataset == "condor":
            self.url_column = "clean_url"
            self.id_column = "url_rid"
            self.date_column = "first_post_time"
            self.date_format = "%Y-%m-%d %H:%M:%S.%f"
        elif dataset == "defacto":
            self.url_column = "claim-review_itemReviewed_appearance_url"
            self.id_column = "id"
            self.date_column = "claim-review_itemReviewed_datePublished"
            self.date_format = "%Y-%m-%dT%H:%M:%S.%f%z"
        elif dataset == "science":
            self.url_column = "url"
            self.id_column = "id"
            self.date_column = "publishedDate"
            self.date_format = "%Y-%m-%dT%H:%M:%S%z"


@click.command
@click.option("--dataset", type=click.Choice(['condor', 'science', 'defacto'], case_sensitive=False), required=True, help="Origin of the data.")
@click.option("--filepath", type=click.Path(exists=True, file_okay=True), required=True, help="CSV file to be added to the collection.")
@click.option("--length", type=int, nargs=1, required=False, help="Length of the CSV file to be added.")
@click.option("--merged-table", "merged_table", type=click.Path(exists=True, file_okay=True), required=False, help="Collection of misinformation sources.")
def main(dataset:str, filepath:str, length:str, merged_table:str):

    # Determine which column in the dataset has the URL
    if dataset != "condor" and dataset != "defacto" and dataset != "science":
        raise ValueError("Dataset must be declared as 'condor', 'defacto', or 'science'.\n")
    
    fields = Fields(dataset)

    # If adding to a previously merged table, serialize the merged table's rows in an indexed dictionary
    index_of_merged_table = {}
    if merged_table:
        with open(merged_table, "r", encoding="utf-8") as open_merged_table:
            merged_table_reader = csv.DictReader(open_merged_table)
            [index_of_merged_table.update({row["url_id"]:row}) for row in merged_table_reader]
    
    # Generate information for new merged table
    if not os.path.isdir("output"):
        os.mkdir("output")
    new_merged_table_name = FileNaming("misinformation", "output", "csv").todays_date
    merged_fieldnames = SHARED_FIELDS+[f"condor_{field}" for field in CONDOR_FIELDS if field!="hash" and field!="normalized_url"]+[f"science_{field}" for field in SCIENCE_FIELDS if field!="hash" and field!="normalized_url"]+[f"defacto_{field}" for field in DEFACTO_FIELDS if field!="hash" and field!="normalized_url"]

    # Open incoming dataset and new merged table
    with open(filepath, "r", encoding="utf-8") as open_dataset, open(new_merged_table_name, "w", encoding="utf-8") as open_new_merge:
        reader = csv.DictReader(open_dataset)
        if length:
            generator = tqdm(reader, total=int(length), desc="Updating collection")
        else:
            generator = reader
        writer = csv.DictWriter(open_new_merge, fieldnames=merged_fieldnames)
        writer.writeheader()

        for row in generator:
            row_hash = row['hash']
            row_normalized_url = row['normalized_url']

            # Format the value in the row's date column
            if row[fields.date_column]:
                row_date = datetime.strptime(row[fields.date_column], fields.date_format)
                row_date = datetime.strptime(row_date.strftime(fields.merged_date_format), fields.merged_date_format)
            else:
                row_date = None

            # Empty dictionary on which to map updated row data 
            merged_row = {"url_id":None, "date":None, "sources":None, "normalized_url":None, "archive_url":None, "archive_timestamp":None}

            # If the merged table does not have a URL with this hash, create a new row
            if row_hash not in index_of_merged_table.keys():
                [merged_row.update({f"{dataset}_{col}":row[col]}) for col in reader.fieldnames if col!="hash" and col!="normalized_url"]
                merged_row.update({"url_id":row_hash, "sources":dataset, "normalized_url":row_normalized_url, "archive_url":row[fields.url_column]})
                index_of_merged_table.update({merged_row["url_id"]:merged_row})
                if row_date:
                    merged_row.update({"date":row_date})

            # If the merged table has a URL with this hash already, update the row
            else:

                existing_row = index_of_merged_table[row_hash]
                merged_row.update(existing_row)

                # Replace the value in the date column with the earliest datetime object
                if isinstance(row_date, datetime):
                    if existing_row.get("date"):
                        if not isinstance(existing_row["date"], datetime):
                            existing_row_date = datetime.strptime(existing_row["date"], fields.merged_date_format)
                        else:
                            existing_row_date = existing_row["date"]
                    if existing_row_date > row_date:
                        merged_row.update({"date":row_date})
                else:
                    merged_row.update({"date":row_date})


                # If the dataset's data hasn't been entered into the merged table, update the sources column with it
                if dataset not in existing_row["sources"]:
                    sources:list = existing_row["sources"].split("|")
                    sources.append(dataset)
                    updated_sources = "|".join(sources)
                    merged_row.update({"sources":updated_sources})

                # Determine if this exact item (via ID) from the incoming dataset has already been entered in the merged table
                dataset_id_col = f"{dataset}_{fields.id_column}"
                if existing_row[dataset_id_col]:
                    ids = existing_row[dataset_id_col].split("|")
                else:
                    ids = []
                # If the dataset's item hasn't been entered in the merged table, update the row
                if row[fields.id_column] not in ids:
                    cols_to_update = [col for col in reader.fieldnames if col!="hash"and col!="normalized_url"]
                    for col in cols_to_update:
                        merged_col = f"{dataset}_{col}"
                        data = existing_row[merged_col]
                        if data:
                            data = data.split("|")
                            data.append(row[col])
                            update = "|".join(data)
                        else:
                            update = row[col]
                        merged_row.update({merged_col:update})
                    index_of_merged_table.update({merged_row["url_id"]:merged_row})

        # Write the new aggregation of hashed URLs
        print(f"Writing new merged table of misinformation sources to file: {new_merged_table_name}")
        writer.writerows(index_of_merged_table.values())


if __name__ == "__main__":
    main()
