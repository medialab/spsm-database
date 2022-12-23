import csv
import json
import os
import sys
import time
from datetime import date

import click
import requests
from minet.utils import md5
from tqdm.auto import tqdm
from ural import is_url, normalize_url

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from src.utils import FileNaming

appearances_directory = os.path.join("data", "sf_appearances")
SCIENCE_FIELDS = ['id', 'hash', 'normalized_url', 'urlContentId', 'url', 'claimReviewed', 'publishedDate', 'publisher', 'reviews_author', 'reviews_reviewRatings_ratingValue', 'reviews_reviewRatings_standardForm', 'urlReviews_reviewRatings_alternateName', 'urlReviews_reviewRatings_ratingValue']


@click.group()
@click.argument("config", required=True, nargs=1)
@click.pass_context
def cli(ctx, config):
    with open(config, "r", encoding="utf-8") as opened_config:
        ctx.obj = json.load(opened_config)["science-feedback"]


@cli.command()
@click.pass_context
@click.option("--start", required=True, nargs=1, help="YYYY-MM-DD")
@click.option("--end", required=True, nargs=1, help="YYYY-MM-DD")
@click.option("--pages", required=True, nargs=1, type=int)
def request(ctx, start, end, pages):

    try:
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
    except:
        raise ValueError("Dates entered were not in the format YYYY-MM-DD.")
    if not start_date < end_date:
        raise ValueError("Start date does not precede end date.")

    if not os.path.isdir("data"):
        os.mkdir("data")
    if not os.path.isdir(appearances_directory):
        os.mkdir(appearances_directory)

    token = ctx.obj["token"]

    for i in tqdm(range(pages), total=pages, desc="Requesting pages"):
        i += 1
        request_url = f"https://api.feedback.org/appearances?page={i}&paginator=100&startPublishedDate={start_date}&endPublishedDate={end_date}"
        attempts = 0
        response = requests.get(request_url, headers={"X-Access-Tokens": token})
        while response.status_code != 200 and attempts < 3 :
            time.sleep(1)
            response = requests.get(request_url, headers={"X-Access-Tokens": token})
            attempts += 1
        data = response.json()

        if len(data) == 0:
            print("The results of this page are empty. The program is exiting.")
            quit()

        outfile = f"page={i}&paginator=100&startPublishedDate={start_date}&endPublishedDate={end_date}"
        with open(os.path.join(appearances_directory, outfile), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


@cli.command()
@click.option("--appearances", "directory", required=False, default=appearances_directory, nargs=1)
@click.pass_context
def flatten(ctx, directory):

    if not os.path.isdir(directory):
        raise NotADirectoryError
    else:
        files = os.listdir(directory)

    token = ctx.obj["token"]
    if not os.path.isdir("data"):
        os.mkdir("data")
    outfile_path = FileNaming(title="sf_flattened", dir="data").todays_date

    with open(outfile_path, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SCIENCE_FIELDS)
        writer.writeheader()

        for file in tqdm(files, total=len(files), desc="Processing pages of results"):
            with open(os.path.join(directory, file), "r", encoding="utf-8") as opened_file:

                page_results = json.load(opened_file)

                for appearance in page_results:

                    request_url = "https://api.feedback.org/appearances/{id}".format(id=appearance.get("id"))
                    attempts = 0

                    response = requests.get(request_url, headers={"X-Access-Tokens": token})
                    while response.status_code != 200 and attempts < 3 :
                        time.sleep(1)
                        response = requests.get(request_url, headers={"X-Access-Tokens": token})
                        attempts += 1

                    data = response.json()

                    if data.get("url") and is_url(data["url"]):
                        appearance_data = AppearanceData(data)
                        urlContentId = appearance.get("urlContentId")
                        writer.writerow(appearance_data.mapping(urlContentId))
 

class AppearanceData:
    def __init__(self, data):
        self.claimReviewed = data.get("claimReviewed")
        self.id = data.get("id")
        self.publishedDate = data.get("publishedDate")
        self.publisher = data.get("publisher")
        self.url = data.get("url")
        self.normalized_url = normalize_url(self.url)
        self.hash = md5(self.normalized_url)
        self.reviews_author = None
        self.reviews_reviewRatings_ratingValue = None
        self.reviews_reviewRatings_standardForm = None
        self.urlReviews_reviewRatings_alternateName = None
        self.urlReviews_reviewRatings_ratingValue = None
        self.urlContentId = None

        reviews = data.get("reviews")
        if reviews:
            self.reviews_author = reviews[0].get("author")
            if reviews[0].get("reviewRatings"):
                self.reviews_reviewRatings_ratingValue = reviews[0].get("reviewRatings")[0].get("ratingValue")
                self.reviews_reviewRatings_standardForm = reviews[0].get("reviewRatings")[0].get("standardForm")
        urlReviews = data.get("urlReviews")
        if urlReviews and urlReviews[0].get("reviewRatings"):
            self.urlReviews_reviewRatings_alternateName = urlReviews[0].get("reviewRatings")[0].get("alternateName")
            self.urlReviews_reviewRatings_ratingValue = urlReviews[0].get("reviewRatings")[0].get("ratingValue")

    def mapping(self, urlContentId:str):
        return {
            "id":self.id,
            "urlContentId":urlContentId,
            "hash":self.hash,
            "claimReviewed":self.claimReviewed,
            "publishedDate":self.publishedDate,
            "publisher":self.publisher,
            "reviews_author":self.reviews_author,
            "reviews_reviewRatings_ratingValue":self.reviews_reviewRatings_ratingValue,
            "reviews_reviewRatings_standardForm":self.reviews_reviewRatings_standardForm,
            "url":self.url,
            "normalized_url":self.normalized_url,
            "urlReviews_reviewRatings_alternateName":self.urlReviews_reviewRatings_alternateName,
            "urlReviews_reviewRatings_ratingValue":self.urlReviews_reviewRatings_ratingValue
        }

if __name__ == "__main__":
    cli()
