from ingestion_scripts.condor import insert as create_condor
from ingestion_scripts.de_facto import insert as create_de_facto
from ingestion_scripts.science_feedback import insert as create_science
from ingestion_scripts.completed_urls_dataset import insert as create_completed_urls
from ingestion_scripts.supplemental_titles import (
    create_supplemental_titles_dataset_table,
)
from ingestion_scripts.title_query import insert as create_title_query_dataset_table
from ingestion_scripts.url_query import insert as create_url_query_dataset_table
