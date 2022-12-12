import csv
import os

import click
from minet.utils import md5
from tqdm.auto import tqdm
from ural import normalize_url

from utils import FileNaming

SHARED_FIELDS = ["url_id", "sources", "normalized_url", "archive_timestamp"]
DEFACTO_FIELDS = ['id', 'themes', 'tags', 'claim-review_claimReviewed', 'claim-review_itemReviewed_datePublished', 'claim-review_itemReviewed_appearance_url', 'claim-review_itemReviewed_appearance_headline', 'claim-review_reviewRating_ratingValue', 'claim-review_reviewRating_alternateName']
SCIENCE_FIELDS = ['id', 'urlContentId', 'url', 'claimReviewed', 'publishedDate', 'publisher', 'reviews_author', 'reviews_reviewRatings_ratingValue', 'reviews_reviewRatings_standardForm', 'urlReviews_reviewRatings_alternateName', 'urlReviews_reviewRatings_ratingValue']
CONDOR_FIELDS = ["url_rid", "clean_url", "first_post_time", "share_title", "tpfc_rating", "tpfc_first_fact_check", "public_shares_top_country"]


@click.command
@click.option("--dataset", type=click.Choice(['condor', 'science', 'defacto'], case_sensitive=False), required=True, help="Origin of the data.")
@click.option("--filepath", type=click.Path(exists=True, file_okay=True), required=True, help="CSV file to be added to the collection.")
@click.option("--length", type=int, nargs=1, required=False, help="Length of the CSV file to be added.")
@click.option("--merged-table", "merged_table", type=click.Path(exists=True, file_okay=True), required=False, help="Collection of misinformation sources.")
def main(dataset:str, filepath:str, length:str, merged_table:str):

    # Determine which column in the dataset has the URL
    if dataset == "defacto":
        url_column = "claim-review_itemReviewed_appearance_url"
        id_column = "id"
    elif dataset == "science":
        url_column = "url"
        id_column = "id"
    elif dataset == "condor":
        url_column = "clean_url"
        id_column = "url_rid"
    else:
        raise ValueError("Dataset must be declared as 'defacto', 'science', or 'condor'.\n")

    # If adding to a previously merged table, serialize the merged table's rows in an indexed dictionary
    index_of_existing_merged_table = {}
    if merged_table:
        with open(merged_table, "r", encoding="utf-8") as open_merged_table:
            merged_table_reader = csv.DictReader(open_merged_table)
            [index_of_existing_merged_table.update({row["url_id"]:row}) for row in merged_table_reader]
    
    # Generate information for new merged table
    new_merged_table_name = FileNaming("misinformation", "data", "csv").todays_date
    merged_fieldnames = SHARED_FIELDS+[f"condor_{field}" for field in CONDOR_FIELDS]+[f"science_{field}" for field in SCIENCE_FIELDS]+[f"defacto_{field}" for field in DEFACTO_FIELDS]

    # Open incoming dataset and new merged table
    with open(filepath, "r", encoding="utf-8") as open_dataset, open(new_merged_table_name, "w", encoding="utf-8") as open_new_merge:
        reader = csv.DictReader(open_dataset)
        if length:
            generator = tqdm(reader, total=int(length), desc="Updating collection")
        else:
            generator = reader
        writer = csv.DictWriter(open_new_merge, fieldnames=merged_fieldnames)
        writer.writeheader()

        # Prepare an empty set for hashed URLs from the dataset
        index_of_dataset = set()

        for row in generator:

            # Empty dictionary on which to map updated row data 
            merged_row = {}

            # Hash the row's URL and update the set of the dataset's hashed URLS
            normalized_url = normalize_url(row[url_column])
            normalized_url_hash = md5(normalized_url)
            index_of_dataset.add(normalized_url_hash)

            # If the existing merged table does not have a URL with this hash, create a new row
            if normalized_url_hash not in index_of_existing_merged_table.keys():
                [merged_row.update({f"{dataset}_{col}":row[col]}) for col in reader.fieldnames]
                merged_row.update({"url_id":normalized_url_hash, "sources":dataset, "normalized_url":normalized_url})
                writer.writerow(merged_row)
            
            # If the existing merged table has a URL with this hash, update the row
            else:
                existing_row = index_of_existing_merged_table[normalized_url_hash]
                merged_row.update(existing_row)

                # If the dataset's data hasn't been entered into the merged table, update the sources column with it
                if dataset not in existing_row["sources"]:
                    sources:list = existing_row["sources"].split("|")
                    sources.append(dataset)
                    updated_sources = "|".join(sources)
                    merged_row.update({"sources":updated_sources})
                else:
                    dataset_id_col = f"{dataset}_{id_column}"
                    ids = existing_row[dataset_id_col].split("|")
                    # If the row's data hasn't been entered into the merged table, update the the columns dedicated to the dataset
                    if row[id_column] not in ids:
                        for col in reader.fieldnames:
                            merged_col = f"{dataset}_{col}"
                            data = existing_row[merged_col].split("|")
                            data.append(row[col])
                            update = "|".join(data)
                            merged_row.update({merged_col:update})
                writer.writerow(merged_row)
            
        # Add to the new collection every row from the previous collection that wasn't in / updated from the dataset
        if merged_table:
            [writer.writerow(index_of_existing_merged_table[i]) for i in list(set(index_of_existing_merged_table.keys())-index_of_dataset)]

    if os.path.isfile(new_merged_table_name):
        print(f"Wrote new merged table of misinformation sources to file: {new_merged_table_name}")

if __name__ == "__main__":
    main()
