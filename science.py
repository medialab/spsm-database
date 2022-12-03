import csv
import json
import os
from datetime import date
import time

from tqdm.auto import tqdm

import click
import requests
from ural import is_url


@click.command()
@click.argument("directory", required=True, nargs=1)
@click.argument("configfile", required=True, nargs=1)
@click.option("--outfile", default=f"science-feedback_{date.today()}.csv")
def cli(directory, configfile, outfile):

    with open(configfile, "r", encoding="utf-8") as opened_config:
        config = json.load(opened_config)["science-feedback"]

    if not os.path.isdir(directory):
        raise NotADirectoryError
    else:
        files = os.listdir(directory)
    
    with open(outfile, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["urlContentId", "appearanceId", "claimReviewed", "publishedDate", "publisher", "url", "title", "urlReviewAlternateName", "urlReviewRatingValue", "reviewsStandardForm", "reviewsRatingValue"])
        writer.writeheader()

        for file in files:
            with open(os.path.join(directory, file), "r", encoding="utf-8") as opened_file:

                deseriealized_data = json.load(opened_file)

                for i in tqdm(deseriealized_data, total=len(deseriealized_data), desc=f"Processing {file}"):

                    attempts = 0
                    response = requests.models.Response()
                    response.status_code = 400
                    while response.status_code != 200 and attempts < 3 :
                        response = requests.get(
                        "{endpoint}{id}".format(endpoint=config["endpoint"], id=i.get("urlContentId")),
                        headers={"X-Access-Tokens": config["token"]},)
                        attempts += 1
                        time.sleep(1)

                    json_response = response.json()

                    if not json_response.get("appearances"):
                        continue

                    else:
                        for appearance in json_response["appearances"]:

                            if appearance.get("urlReviews") and len(appearance["urlReviews"]) == 1 and appearance["urlReviews"][0].get("reviewRatings") and len(appearance["urlReviews"][0]["reviewRatings"]) == 1:
                                urlReviewAlternateName = appearance["urlReviews"][0]["reviewRatings"][0].get("alternateName")
                                urlReviewRatingValue = appearance["urlReviews"][0]["reviewRatings"][0].get("ratingValue")
                            
                            else:
                                urlReviewAlternateName = None
                                urlReviewRatingValue = None

                            if appearance.get("reviews") and len(appearance["reviews"]) == 1 and appearance["reviews"][0].get("reviewRatings") and len(appearance["reviews"][0]["reviewRatings"]) == 1:
                                reviewsStandardForm = appearance["reviews"][0]["reviewRatings"][0].get("standardForm")
                                reviewsRatingValue = appearance["reviews"][0]["reviewRatings"][0].get("ratingValue")

                            else:
                                reviewsStandardForm = None
                                reviewsRatingValue = None

                            if is_url(json_response.get("url")):
                                writer.writerow(
                                    {
                                        "urlContentId":json_response.get("id"),
                                        "claimReviewed":appearance.get("claimReviewed"),
                                        "url":json_response.get("url"),
                                        "title":json_response.get("title"),
                                        "appearanceId":appearance.get("id"),
                                        "publishedDate":appearance.get("publishedDate"),
                                        "publisher":appearance.get("publisher"),
                                        "urlReviewAlternateName":urlReviewAlternateName,
                                        "urlReviewRatingValue":urlReviewRatingValue,
                                        "reviewsStandardForm":reviewsStandardForm,
                                        "reviewsRatingValue":reviewsRatingValue
                                    }
                                )

if __name__ == "__main__":
    cli()
