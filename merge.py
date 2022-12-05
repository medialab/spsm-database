import csv
import os
from datetime import date

import click
from minet.utils import md5
from tqdm.auto import tqdm
from ural import normalize_url

SHARED_FIELDS = ["id", "sources", "url", "normalized_url", "normalized_url_hash", "title", "date", "review"]
DEFACTO_FIELDS = ["id", "url", "claimReviewed", "datePublished", "alternateName", "themes", "tags", "ratingValue"]
SCIENCE_FIELDS = ["urlContentId", "appearanceId", "claimReviewed", "publishedDate", "publisher", "url", "title", "urlReviewAlternateName", "urlReviewRatingValue", "reviewsStandardForm", "reviewsRatingValue"]
CONDOR_FIELDS = ["url_rid", "clean_url", "first_post_time", "share_title", "tpfc_rating", "tpfc_first_fact_check", "public_shares_top_country"]


class CSVFileError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

    def __str__(self) -> str:
        return super().__str__()

class DataSetError(Exception):
    def __init__(self, *args: object):
        super().__init__(*args)

    def __str__(self) -> str:
        return super().__str__()


class Collection:
    def __init__(self, collection:str):
        """Inspect in- and out-files."""
        
        # Inspect the in-file
        if not collection or csv.DictReader(open(collection, "r")).fieldnames != self.merged_fieldnames():
            self.current_collection = None
            self.length = None
        else:
            self.current_collection = collection
            with open(self.current_collection, "r") as open_csv:
                reader = csv.DictReader(open_csv)
                for row in reader: pass
                self.length = reader.line_num

        # Name the out-file
        today_csv = f"misinformation_sources_{date.today()}.csv"
        if self.current_collection and os.path.basename(self.current_collection) == today_csv:
            basename = os.path.basename(self.current_collection)
            if len(basename.split("_")[-1].split("-")) == 3:
                self.new_file = f"misinformation_sources_{date.today()}_2.csv"
            else:
                try:
                    suffix = int(basename.split("_").pop())
                    self.new_file = f"misinformation_sources_{date.today()}_{suffix+1}.csv"
                except:
                    self.new_file = f"misinformation_sources_{date.today()}_2.csv"
        elif os.path.isfile(today_csv):
            i = 2
            while os.path.isfile(f"misinformation_sources_{date.today()}_{i}.csv"):
                i+=1
            self.new_file = f"misinformation_sources_{date.today()}_{i}.csv"
        else:
            self.new_file = today_csv
    
    def merged_fieldnames(self):
        """Create array of fieldnames for the merged collection of misinformation sources."""
        defacto_fileds = [f"defacto_{field}" for field in DEFACTO_FIELDS]
        science_fields = [f"science_{field}" for field in SCIENCE_FIELDS]
        condor_fields = [f"condor_{field}" for field in CONDOR_FIELDS]
        return SHARED_FIELDS+condor_fields+science_fields+defacto_fileds
    
    def index_by_hash(self):
        """From the current collection, store every row as a dictionary whose key is the hashed URL."""
        indexed_rows = {}
        if self.current_collection:
            with open(self.current_collection, "r", encoding="utf-8") as opened_csv:
                if self.length:
                    reader = tqdm(csv.DictReader(opened_csv), total=self.length, desc="Indexing collection")
                else:
                    reader = csv.DictReader(opened_csv)
                for row in reader:
                    indexed_rows.update({row["normalized_url_hash"]:row})
        return indexed_rows


class DataSet:
    def __init__(self, file:str, dataset:str):
        """Inspect the in-file and the declared dataset."""
        self.dataset = dataset

        if self.dataset == "defacto" or self.dataset == "science": self.url_column = "url"
        elif self.dataset == "condor": self.url_column = "clean_url"
        else: raise DataSetError("Data must be declared as 'defacto', 'science', or 'condor'.\n")

        # Inspect the in-file
        if not os.path.isfile(file):
            raise FileExistsError
        try:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                assert len(reader.fieldnames) > 2
                self.fp = file
        except:
            raise CSVFileError("File is not CSV with multiple headers.\n")

    def prefix(self, row):
        """Add a prefix to the in-file row's column headers and add data fields for the normalized URL and hash."""
        row = {f"{self.dataset}_{key}": val for key, val in row.items()}
        new_url_fieldname = f"{self.dataset}_{self.url_column}"
        normalized_url = normalize_url(row[new_url_fieldname])
        normalized_url_hash = md5(normalized_url)
        row.update({"normalized_url":normalized_url, "normalized_url_hash":normalized_url_hash})
        return row

    def reader(self):
        """Generate a CSV reader of the in-file."""
        with open(self.fp, "r", encoding="utf-8") as opened_csv:
            yield from csv.DictReader(opened_csv)
    

@click.command
@click.option("--dataset", type=click.Choice(['condor', 'science', 'defacto'], case_sensitive=False), required=True, help="Origin of the data.")
@click.option("--file", type=click.Path(exists=True, file_okay=True), required=True, help="CSV file to be added to the collection.")
@click.option("--length", "length", required=False, help="Length of the CSV file to be added.")
@click.option("--collection", type=click.Path(exists=True, file_okay=True), required=False, help="Collection of misinformation sources.")
def main(dataset:str, file:str, length:str, collection:str):

    # Initially parse the dataset and, if applicable, the existing collection
    dataset_data = DataSet(file, dataset)
    collection_data = Collection(collection=collection)

    # If a collection exists, index its data, otherwise return empty dictionary
    collection_index = collection_data.index_by_hash()

    if length:
        reader = tqdm(dataset_data.reader(), total=int(length), desc="Updating collection")
    else:
        reader = dataset_data.reader()

    with open(collection_data.new_file, "w", encoding="utf-8") as opened_csv:
        writer = csv.DictWriter(opened_csv, fieldnames=collection_data.merged_fieldnames())
        writer.writeheader()

        # Prepare an empty set for hashed URLs from the dataset
        dataset_index_hashes = set()

        for row in reader:
            # Make the row's data compatible with the merged colletion's fieldnames
            compatible_row = dataset_data.prefix(row)

            # Update the set with the row's hashed URL
            dataset_index_hashes.add(compatible_row["normalized_url_hash"])

            # If the existing collection does not have a URL with this hash, create a new row
            if compatible_row["normalized_url_hash"] not in collection_index.keys():

                if dataset == "defacto":
                    map_shared_fieldnames = {
                        "id":compatible_row["normalized_url_hash"], 
                        "sources":"defacto", 
                        "url":compatible_row["defacto_url"], 
                        "title":compatible_row["defacto_claimReviewed"], 
                        "date":compatible_row["defacto_datePublished"], 
                        "review":compatible_row["defacto_alternateName"]
                    }
                elif dataset == "condor":
                    map_shared_fieldnames = {
                        "id":compatible_row["normalized_url_hash"],
                        "sources":"condor",
                        "url":compatible_row["condor_clean_url"],
                        "title":compatible_row["condor_share_title"],
                        "date":compatible_row["condor_first_post_time"],
                        "review":compatible_row["condor_tpfc_rating"]
                    }
                elif dataset == "science":
                    if compatible_row["science_urlReviewAlternateName"]:
                        review = compatible_row["science_urlReviewAlternateName"]
                    else:
                        compatible_row["science_reviewsStandardForm"]
                    map_shared_fieldnames = {
                        "id":compatible_row["normalized_url_hash"],
                        "sources":"science_feedback",
                        "url":compatible_row["science_url"],
                        "title":compatible_row["science_title"],
                        "date":compatible_row["science_publishedDate"],
                        "review":review
                    }
                else:
                    map_shared_fieldnames = {}
                    raise DataSetError("Data must be declared as 'defacto', 'science', or 'condor'.\n") 
                
                # Map the relevant shared fieldnames to the dataset's fieldnames
                compatible_row.update(map_shared_fieldnames)

                # Write the dataset's updated row to the new collection
                writer.writerow(compatible_row)
            
            # If the existing collection has a URL with this hash, update the row
            else:
                sources = collection_index[compatible_row["normalized_url_hash"]]["sources"].split("|")
                if dataset not in sources:
                    existing_data = collection_index[compatible_row["normalized_url_hash"]]

                    # To the list of sources contributing to this row in the collection, add the new dataset 
                    sources.append(dataset)
                    updated_sources = "|".join(sources)
                    existing_data.update({"sources":updated_sources})

                    # To the row's existing data, add relevant new data from the dataset
                    if dataset == "defacto":
                        map_special_fieldnames = {
                            "defacto_id":compatible_row["defacto_id"], 
                            "defacto_url":compatible_row["defacto_url"],
                            "defacto_claimReviewed":compatible_row["defacto_claimReviewed"],
                            "defacto_datePublished":compatible_row["defacto_datePublished"],
                            "defacto_alternateName":compatible_row["defacto_alternateName"],
                            "defacto_themes":compatible_row["defacto_themes"],
                            "defacto_tags":compatible_row["defacto_tags"],
                            "defacto_ratingValue":compatible_row["defcto_ratingValue"]
                        }
                    elif dataset == "condor":
                        map_special_fieldnames = {
                            "condor_url_rid":compatible_row["condor_url_rid"],
                            "condor_clean_url":compatible_row["condor_clean_url"],
                            "condor_first_post_time":compatible_row["condor_share_title"],
                            "condor_tpfc_rating":compatible_row["condor_tpfc_rating"],
                            "condor_tpfc_first_fact_check":compatible_row["condor_tpfc_first_fact_check"],
                            "condor_public_shares_top_country":compatible_row["condor_public_shares_top_country"],
                        }
                    elif dataset == "science":
                        map_special_fieldnames = {
                            "science_urlContentId":compatible_row["science_urlContentId"],
                            "science_appearanceId":compatible_row["science_appearanceId"],
                            "science_claimReviewed":compatible_row["science_claimReviewed"],
                            "science_publishedDate":compatible_row["science_publishedDate"],
                            "science_publisher":compatible_row["science_publisher"],
                            "science_url":compatible_row["science_url"],
                            "science_title":compatible_row["science_title"],
                            "science_urlReviewAlternateName":compatible_row["science_urlReviewAlternateName"],
                            "science_urlReviewRatingValue":compatible_row["science_urlReviewRatingValue"],
                            "science_reviewsStandardForm":compatible_row["science_reviewsStandardForm"],
                            "science_reviewsRatingValue":compatible_row["science_reviewsRatingValue"],
                        }
                    else:
                        map_special_fieldnames = {}
                        raise DataSetError("Data must be declared as 'defacto', 'science', or 'condor'.\n") 
                    existing_data.update(map_special_fieldnames)
                    writer.writerow(existing_data)
            
        # Add to the new collection every row from the previous collection that wasn't in / updated from the dataset
        if collection_data.current_collection:
            [writer.writerow(collection_index[i]) for i in list(set(collection_index.keys())-dataset_index_hashes)]
        
    if os.path.isfile(collection_data.new_file):
        print(f"Wrote new collection of misinformation sources to file: {collection_data.new_file}")


if __name__ == "__main__":
    main()
