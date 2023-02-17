import csv
import json
import os
import shutil
from collections import namedtuple
from datetime import datetime

import casanova
import click
import requests
from CONSTANTS import DATE_FORMAT, DEFACTO_FIELDS, SCIENCE_FIELDS
from flatten_defacto import ClaimData
from flatten_sciencefeedback import AppearanceData
from tqdm.auto import tqdm
from ural import is_url, normalize_url

# Set up paths for CSV files
TEMP_DIR = os.path.join('.', 'collected-data')
if os.path.isdir(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)
os.makedirs(TEMP_DIR, exist_ok=True)
EnrichedCSVFilePath = namedtuple('EnrichedCSVFilepath', ['science_feedback', 'defacto', 'condor'])
enriched_csv_filepath = EnrichedCSVFilePath(
    science_feedback=os.path.join(TEMP_DIR, 'enriched_science_feedback.csv'),
    defacto=os.path.join(TEMP_DIR, 'enriched_defacto.csv'),
    condor=os.path.join(TEMP_DIR, 'enriched_condor.csv')
)

@click.command()
@click.argument('config-file')
@click.option('--condor-csv')
def main(config_file, condor_csv):

    # ------------------------------------------------------- #
    # 1. Get endpoints and configuration details
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # ------------------------------------------------------- #
    # 2. Based on a hash of the normalized URL, add an ID to each source in Condor dataset
    condor_length = casanova.reader.count(input_file=condor_csv)
    with open(condor_csv, 'r') as f, open(enriched_csv_filepath.condor, 'w') as of:
        enricher = casanova.enricher(f, of, add=['hash'])
        for row, clean_url in tqdm(enricher.cells('clean_url', with_rows=True), desc='Processing Condor dataset', total=condor_length):
            url_id = None
            if is_url(clean_url):
                url_id = normalize_url(clean_url)
            enricher.writerow(row, [url_id])

    # ------------------------------------------------------- #
    # 3. Using the endpoint, request all fact-checked claims from De Facto's database
    endpoint = config['defacto']['endpoint']
    end_date = datetime.strptime(config['defacto']['end_date'], '%Y-%m-%d').isocalendar()
    print('Requesting data from De Facto database')
    response = requests.get(endpoint)
    try:
        data = response.json()['data']
    except:
        raise RuntimeError
    with open(enriched_csv_filepath.defacto, 'w') as of:
        writer = csv.DictWriter(of, fieldnames=DEFACTO_FIELDS)
        writer.writeheader()
        for claim in tqdm(data, total=len(data), desc='Processing De Facto dataset'):
            claim_data = ClaimData(claim)
            if claim_data.url and is_url(claim_data.url) and claim_data.reviewPublished.isocalendar() < end_date:
                writer.writerow(claim_data.mapping())

    # ------------------------------------------------------- #
    # 4. Request apperances of fact-checked claims from Science Feedback's database
    token = config['science-feedback']['token']
    start_date = config['science-feedback']['start_date']
    end_date = config['science-feedback']['end_date']
    nb_pages = int(config['science-feedback']['pages'])
    appearances_dir = os.path.join(TEMP_DIR, 'science_feedback_appearances')
    os.makedirs(appearances_dir, exist_ok=True)
    for page_n in tqdm(range(nb_pages), total=nb_pages, desc='Requesting appearances from Science Feedback'):
        page_n += 1
        endpoint = f'https://api.feedback.org/appearances?page={page_n}&paginator=50&startPublishedDate={start_date}&endPublishedDate={end_date}&startUpdatedDate={start_date}&endUpdatedDate={end_date}'
        response = requests.get(endpoint, headers={'X-Access-Tokens': token})
        data = response.json()

        if len(data) == 0:
            print('The results of this page are emtpy.')
            break
        appearances_results_page = os.path.join(appearances_dir, f'page={page_n}&paginator=50&startPublishedDate={start_date}&endPublishedDate={end_date}.json')
        with open(appearances_results_page, 'w', encoding='utf-8') as of:
            json.dump(data, of, indent=4)

    # ------------------------------------------------------- #
    # 5. Request and process metadata for Science Feedback appearances
    appearances_pages = os.listdir(appearances_dir)
    with open(enriched_csv_filepath.science_feedback, 'w', encoding='utf-8') as of:
        writer = csv.DictWriter(of, fieldnames=SCIENCE_FIELDS)
        writer.writeheader()
        for appearances_page in tqdm(appearances_pages, total=len(appearances_pages), desc='Requesting metadata from Science Feedback'):
            with open(os.path.join(appearances_dir,appearances_page), 'r', encoding='utf-8') as f:
                page_results = json.load(f)
                for appearance in page_results:
                    endpoint = 'https://api.feedback.org/appearances/{id}'.format(id=appearance.get("id"))
                    response = requests.get(endpoint, headers={'X-Access-Tokens':token})
                    data = response.json()
                    if data.get('url') and is_url(data['url']):
                        appearance_metadata = AppearanceData(data)
                        urlContentId = appearance.get('urlContentId')
                        writer.writerow(appearance_metadata.mapping(urlContentId))



if __name__ == "__main__":
    main()