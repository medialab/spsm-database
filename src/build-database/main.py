# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for creating tables and inserting data from CSV files
#
from connection import connection, filepaths
from insert_data.data_sources import insert_data_sources
from insert_data.twitter import insert_tweets


def main():
    if connection:
        insert_data_sources(connection=connection, data=filepaths["data sources"])
        insert_tweets(connection=connection, data=filepaths["tweets"])


if __name__ == "__main__":
    main()
