import csv
import os
import sys

import click
from minet.utils import md5
from ural import is_url, normalize_url

yellow = "\033[1;33m"
green = "\033[0;32m"
reset = "\033[0m"

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from src.utils import FileNaming

CONDOR_FIELDS = ["url_rid", 'hash', 'normalized_url', "clean_url", "first_post_time", "share_title", "tpfc_rating", "tpfc_first_fact_check", "public_shares_top_country"]

class CondorRow():
    def __init__(self,row:dict):
        self.url_rid = row["url_rid"]
        self.clean_url = row["clean_url"]
        self.normalized_url = None
        self.hash = None
        self.first_post_time = row["first_post_time"]
        self.share_title = row["share_title"]
        self.tpfc_rating = row["tpfc_rating"]
        self.tpfc_first_fact_check = row["tpfc_first_fact_check"]
        self.public_shares_top_country = row["public_shares_top_country"]
        if is_url(self.clean_url):
            self.normalized_url = normalize_url(self.clean_url)
            self.hash = md5(self.normalized_url)

    def mapping(self):
        if self.hash:
            return {
                "url_rid":self.url_rid,
                "clean_url":self.clean_url,
                "first_post_time":self.first_post_time,
                "share_title":self.share_title,
                "tpfc_rating":self.tpfc_rating,
                "tpfc_first_fact_check":self.tpfc_first_fact_check,
                "normalized_url":self.normalized_url,
                "public_shares_top_country":self.public_shares_top_country,
                "hash":self.hash
            }


@click.command()
@click.argument("datafile", required=True)
def cli(datafile):

    # Name the outfile
    if not os.path.isdir("data"):
        os.mkdir("data")
    outfile_path = FileNaming(title="condor_cleaned", dir="data").todays_date

    with open(datafile, "r", encoding="utf-8") as open_infile, open(outfile_path, "w", encoding="utf-8") as open_outfile:
        reader = csv.DictReader(open_infile)
        
        fieldnames = ["url_rid", "hash", "normalized_url", "clean_url", "first_post_time", "share_title", "tpfc_rating", "tpfc_first_fact_check", "public_shares_top_country"]
        writer = csv.DictWriter(open_outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Map claims in the dataset and write to the outfile
        for row in reader:
            row_data = CondorRow(row)
            if row_data.hash:
                writer.writerow(row_data.mapping())
        


if __name__ == "__main__":
    cli()
