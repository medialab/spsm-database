import argparse
import csv
import json
import os
import shutil
from collections import namedtuple
from datetime import datetime

import casanova
from CONSTANTS import DEFACTO_FIELDS, SCIENCE_FIELDS
from flatten_defacto import ClaimData
from flatten_sciencefeedback import AppearanceData
from minet.web import request
from minet.utils import md5
from tqdm.auto import tqdm
from ural import is_url, normalize_url

# Set up paths for CSV files
TEMP_DIR = os.path.join("data", "cleaned_sources")
if os.path.isdir(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)
EnrichedCSVFilePath = namedtuple(
    "EnrichedCSVFilepath", ["science_feedback", "defacto", "condor"]
)
today = str(datetime.today().date())
enriched_csv_filepath = EnrichedCSVFilePath(
    science_feedback=os.path.join(TEMP_DIR, f"science_feedback_{today}.csv"),
    defacto=os.path.join(TEMP_DIR, f"defacto_{today}.csv"),
    condor=os.path.join(TEMP_DIR, f"condor_{today}.csv"),
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-file")
    parser.add_argument("--condor-csv")
    parser.add_argument("--sf-appearances")
    args = parser.parse_args()
    config_file, condor_csv, sf_appearances = (
        args.config_file,
        args.condor_csv,
        args.sf_appearances,
    )

    # ------------------------------------------------------- #
    # 1. Get endpoints and configuration details
    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    # ------------------------------------------------------- #
    # 2. Based on a hash of the normalized URL, add an ID to each source in Condor dataset
    condor_length = casanova.reader.count(input_file=condor_csv)
    with open(condor_csv, "r") as f, open(enriched_csv_filepath.condor, "w") as of:
        enricher = casanova.enricher(f, of, add=["hash", "normalized_url"])
        for row, clean_url in tqdm(
            enricher.cells("clean_url", with_rows=True),
            desc="Processing Condor dataset",
            total=condor_length,
        ):
            hash, normalized_url = None, None
            if is_url(clean_url):
                normalized_url = normalize_url(clean_url)
                hash = md5(normalized_url)
            enricher.writerow(row, [hash, normalized_url])

    # ------------------------------------------------------- #
    # 3. Using the endpoint, request all fact-checked claims from De Facto's database
    endpoint = config["defacto"]["endpoint"]
    end_date = datetime.strptime(
        config["defacto"]["end_date"], "%Y-%m-%d"
    ).isocalendar()
    print("Requesting data from De Facto database")

    response = request(url=endpoint)
    data = response.json()
    claims = data["data"]
    with open(enriched_csv_filepath.defacto, "w") as of:
        writer = csv.DictWriter(of, fieldnames=DEFACTO_FIELDS)
        writer.writeheader()
        for claim in tqdm(
            claims, total=len(claims), desc="Processing De Facto dataset"
        ):
            claim_data = ClaimData(claim)
            if (
                claim_data.url
                and is_url(claim_data.url)
                and claim_data.reviewPublished
                and claim_data.reviewPublished.isocalendar() < end_date
            ):
                writer.writerow(claim_data.mapping())

    # ------------------------------------------------------- #
    # 4. Request apperances of fact-checked claims from Science Feedback's database
    token = config["science-feedback"]["token"]
    start_date = config["science-feedback"]["start_date"]
    end_date = config["science-feedback"]["end_date"]
    nb_pages = int(config["science-feedback"]["pages"])
    if sf_appearances:
        appearances_dir = sf_appearances
    else:
        appearances_dir = os.path.join(
            TEMP_DIR, f"science_feedback_appearances_{today}"
        )
        os.makedirs(appearances_dir, exist_ok=True)
        for page_n in tqdm(
            range(nb_pages),
            total=nb_pages,
            desc="Requesting appearances from Science Feedback",
        ):
            page_n += 1
            endpoint = f"https://api.feedback.org/appearances?page={page_n}&paginator=50&startPublishedDate={start_date}&endPublishedDate={end_date}&startUpdatedDate={start_date}&endUpdatedDate={end_date}"
            response = request(url=endpoint, headers={"X-Access-Tokens": token})
            data = response.json()

            if len(data) == 0:
                print("The results of this page are emtpy.")
                break
            appearances_results_page = os.path.join(
                appearances_dir,
                f"page={page_n}&paginator=50&startPublishedDate={start_date}&endPublishedDate={end_date}.json",
            )
            with open(appearances_results_page, "w", encoding="utf-8") as of:
                json.dump(data, of, indent=4)

    # ------------------------------------------------------- #
    # 5. Request and process metadata for Science Feedback appearances
    appearances_pages = os.listdir(appearances_dir)
    with open(enriched_csv_filepath.science_feedback, "w", encoding="utf-8") as of:
        writer = csv.DictWriter(of, fieldnames=SCIENCE_FIELDS)
        writer.writeheader()
        for appearances_page in tqdm(
            appearances_pages,
            total=len(appearances_pages),
            desc="Requesting metadata from Science Feedback",
        ):
            with open(
                os.path.join(appearances_dir, appearances_page), "r", encoding="utf-8"
            ) as f:
                page_results = json.load(f)
                for appearance in page_results:
                    endpoint = "https://api.feedback.org/appearances/{id}".format(
                        id=appearance.get("id")
                    )
                    response = request(url=endpoint, headers={"X-Access-Tokens": token})
                    data = response.json()
                    if (
                        # If data is not found, data = [{'data': ['Not Found']}]
                        isinstance(data, dict)
                        and data.get("url")
                        and is_url(data["url"])
                    ):
                        appearance_metadata = AppearanceData(data)
                        urlContentId = appearance.get("urlContentId")
                        writer.writerow(appearance_metadata.mapping(urlContentId))


if __name__ == "__main__":
    main()
