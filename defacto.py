import requests
import json
import csv
import click
from ural import is_url
from tqdm.auto import tqdm


yellow = "\033[1;33m"
green = "\033[0;32m"
reset = "\033[0m"

from utils import FileNaming


class ClaimData:
    def __init__(self, claim):
        self.id = claim.get("id")
        self.themes = "|".join(claim.get("themes"))
        self.tags = "|".join(claim.get("tags"))
        self.claimReviewed = None
        self.datePublished = None
        self.url = None
        self.headline = None
        self.ratingValue = None
        self.alternateName = None

        if claim.get("claim-review"):
            self.claimReviewed = claim["claim-review"].get("claimReviewed")
            if claim["claim-review"].get("itemReviewed"):
                self.datePublished = claim["claim-review"]["itemReviewed"].get("datePublished")
                self.url = claim["claim-review"]["itemReviewed"]["appearance"].get("url")
                self.headline = claim["claim-review"]["itemReviewed"]["appearance"].get("headline")

        if claim.get("claim-review") and claim["claim-review"].get("reviewRating"):
            self.ratingValue = claim["claim-review"]["reviewRating"].get("ratingValue")
            self.alternateName = claim["claim-review"]["reviewRating"].get("alternateName")
        
    def mapping(self):
        return {
            "id":self.id,
            "themes":self.themes,
            "tags":self.tags,
            "claim-review_claimReviewed":self.claimReviewed,
            "claim-review_itemReviewed_datePublished":self.datePublished,
            "claim-review_itemReviewed_appearance_url":self.url,
            "claim-review_itemReviewed_appearance_headline":self.headline,
            "claim-review_reviewRating_ratingValue":self.ratingValue,
            "claim-review_reviewRating_alternateName":self.alternateName
        }


@click.command()
@click.argument("config", required=True)
def cli(config):

    # Get the endpoint from the configuration file
    with open(config, "r", encoding="utf-8") as opened_config:
        access = json.load(opened_config).get("defacto",{}).get("endpoint")
        if not access:
            raise ValueError("The configuration file does not contain a De Facto endpoint.")

    # Name the outfile
    outfile_path = FileNaming(title="df_flattened", dir="data").todays_date

    # Request data from the database
    print("requesting data")
    response = requests.get(access)
    try:
        data = response.json()["data"]
        print(f"{green}--success--{reset}")
    except:
        raise RuntimeError("The request to De Facto's database failed.")

    with open(outfile_path, "w", encoding="utf-8") as f:
        fieldnames = ["id", "themes", "tags", "claim-review_claimReviewed", "claim-review_itemReviewed_datePublished", "claim-review_itemReviewed_appearance_url", "claim-review_itemReviewed_appearance_headline", "claim-review_reviewRating_ratingValue", "claim-review_reviewRating_alternateName"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        # Map claims in the dataset and write to the outfile
        for claim in tqdm(data, total=len(data), desc="Processing claims"):
            data = ClaimData(claim)
            if data.url and is_url(data.url):
                writer.writerow(data.mapping())


if __name__ == "__main__":
    cli()
    