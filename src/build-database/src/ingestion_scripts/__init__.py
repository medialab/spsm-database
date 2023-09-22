from ingestion_scripts.condor import insert as create_condor
from ingestion_scripts.de_facto import insert as create_de_facto
from ingestion_scripts.science_feedback import insert as create_science
from ingestion_scripts.completed_urls_dataset import insert as create_completed_urls
from ingestion_scripts.searchable_titles_urls import (
    insert as create_searchable_titles_urls,
)
from ingestion_scripts.enriched_titles import setup_enriched_title_dataset_table
