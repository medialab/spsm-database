# Database

The database is built with scripts in this directory. To observe the database's creation locally, install PostgreSQL and create a database ("spsm"). You will need to modify the [example configuration YAML](example.config.json) so that it has details about your connection to the PostgreSQL database as well as paths to all the files necessary for data ingestion, which are listed in the example configuration YAML and detailed below.

Steps:

1. [Installation and set up](#set-up)
1. [Ingest original data sources into database](#step-1-ingest-original-data-sources)
1. [Merge data sources into central claims table](#step-2-merge-data-sources)

## Step 1. Ingest original data sources

```
Usage: ingest.py [OPTIONS] CONFIG

  Main function to manage the ingestion of raw data to the database. Data can
  come from CSV files or JSON files. Paths to these files must be declared in
  the configuration YAML, which is this command's first and only positional
  argument.

Options:
  --data-source [condor|de facto|science feedback|completed urls]
  --no-prompt                     Skip the prompt that asks the user to
                                  double-check the path to the data file.
  --help                          Show this message and exit.
```

### Configuration YAML

The configuration YAML has 2 top-level keys, `connection` and `data sources`. The first contains information necessary for Python to connect to the PostgreSQL server. The second provides paths to the files whose data will be transformed and used to construct the database's tables. These file paths are recorded in the configuration YAML because the data files upon which the database is built should never be altered. In our case, each file necessary for the data ingestion phase is stored in a private repository, whose links are given below (and accessible only to group members).

- `condor`: [Link to CSV](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/condor_full.csv) (rows: 101422)
  - data delivered in summer 2022
- `science feedback`: [Link to JSON](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/science_feedback_full.json)
  - data collected from API in fall 2022, re-requested in spring 2023
- `de facto`: [Link to JSON](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/defacto_full.json)
  - data collected from API in fall 2022, re-requested in spring 2023
- `enriched titles`: [Link to CSV](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/url_title_enrichment.csv) (rows: 110166)
  - all data sources' URLs, normalized and de-duplicated
  - each normalized URL is associated with (a) a non-normalized version used for achiving, `archive_url`, and (b) titles:
    - `condor_share_title`: provided by Condor dataset
    - `yt_video_headline`: requested from YouTube API
    - `webpage_title`: scraped from HTML
    - `webarchive_search_title`: recovered from Web Archive
- `completed urls`: [Link to CSV](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/unique_completed_urls_from_condor_set_of_duplicate_urls.csv) (rows: 612)
  - URLs manually constructed from impoverished URLs
  - accompanying metadata (i.e. `condor_id`) is from Condor because impoverished URLs were selected from Condor dataset

### Ingestion commands

- Ingest Condor data

  - `python ingest.py --data-source condor`
  - necessary files (YAML): `condor`, `enriched titles`
  - yields tables "dataset_condor", "dataset_enriched_titles"

- Ingest De Facto data

  - `python ingest.py --data-source de facto`
  - necessary files (YAML): `de facto`, `enriched titles`
  - yields tables "dataset_de_facto", "dataset_enriched_titles"

- Ingest Science Feedback data

  - `python ingest.py --data-source science feedback`
  - necessary files (YAML): `science feedback`, `enriched titles`
  - yields tables "dataset_science_feedback", "dataset_enriched_titles"

- Ingest manually completed URLs dataset
  - `python ingest.py --data-source completed urls`
  - necessary files (YAML): `completed urls`
  - necessary tables: "dataset_condor"
  - yields table "dataset_completed_urls"

## Step 2. Merge data sources

## Set Up

Set up the Python environment.

1. Install Python version 3.11
2. Create and activate a virtual environment.
3. Install dependencies. `pip install -r sql-requirements.txt`

Set up the connection to a PostgreSQL server and create a database. Record details of this connection and the database's name in the [configuration file](example.config.json).
