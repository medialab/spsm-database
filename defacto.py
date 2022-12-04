import requests
import json
import time
import csv
import click
from ural import is_url
from datetime import date


yellow = "\033[1;33m"
green = "\033[0;32m"
reset = "\033[0m"


class DeFactoJSON:
    def __init__(self, config):
        with open(config, "r", encoding="utf-8") as opened_config:
            access = json.load(opened_config)["defacto"]
        self.access = access

    def load_data(self):
        attempts = 0
        response = requests.models.Response()
        response.status_code = 400
        while response.status_code != 200 and attempts < 10 :
            print("Attempt {} to request data from {}.".format(attempts+1, self.access))
            response = requests.get(self.access)
            attempts += 1
            time.sleep(1)
        if response.status_code != 200:
            print("The request to the API was not successful. Try again later.")
        else:
            print(f"{green}Received good response from data source.{reset}")
            return json.loads(response.text)


class DeFactoData:
    def __init__(self, claim):
        self.id = claim.get("id")
        self.themes = "|".join(claim.get("themes"))
        self.tags = "|".join(claim.get("tags"))
        self.claimReviewed = None
        self.datePublished = None
        self.url = None
        self.ratingValue = None
        self.alternateName = None

        if claim.get("claim-review"):
            self.claimReviewed = claim["claim-review"].get("claimReviewed")
            if claim["claim-review"].get("itemReviewed"):
                self.datePublished = claim["claim-review"]["itemReviewed"].get("datePublished")
                self.url = claim["claim-review"]["itemReviewed"]["appearance"].get("url")

        if claim.get("claim-review") and claim["claim-review"].get("reviewRating"):
            self.ratingValue = claim["claim-review"]["reviewRating"].get("ratingValue")
            self.alternateName = claim["claim-review"]["reviewRating"].get("alternateName")


@click.command()
@click.argument("config", required=True)
@click.option("--outfile", default=f"defacto_{date.today()}.csv")
def cli(config, outfile):
    data = DeFactoJSON(config).load_data()

    rows = [{"id":DeFactoData(claim).id, "claimReviewed":DeFactoData(claim).claimReviewed, "themes":DeFactoData(claim).themes, "tags":DeFactoData(claim).tags, "datePublished":DeFactoData(claim).datePublished, "url":DeFactoData(claim).url, "ratingValue":DeFactoData(claim).ratingValue, "alternateName":DeFactoData(claim).alternateName} \
        for claim in data["data"] if DeFactoData(claim).url and is_url(DeFactoData(claim).url)]

    with open(outfile, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "claimReviewed", "themes", "tags", "datePublished", "url", "ratingValue", "alternateName"])
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    cli()
    