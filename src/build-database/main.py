# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for creating tables and inserting data from CSV files
#
import csv

import casanova
from tqdm import tqdm

from connection import connection, filepaths
from tables.schemas import TweetQueryTable, TweetTable, TwitterUserTable


def main():
    if connection:
        # Get paths to tweet data from the config file
        tweet_files = filepaths["tweets"]

        # Instantiate the tweet, user, and tweet-query relation tables
        tweet_table = TweetTable()
        tweet_query_table = TweetQueryTable()
        twitter_user_table = TwitterUserTable()
        tables = [twitter_user_table, tweet_table, tweet_query_table]

        # (create and drop tables to clear database and start fresh)
        for table in tables:
            table.create(connection=connection)
        for table in tables:
            table.drop(connection=connection, force=True)

        # Create tables
        for table in tables:
            print(f"(Re)creating table: {table.name}")
            table.create(connection=connection)

        # Ingest data
        for file in tweet_files:
            print(f"\nInserting data from: {file}")
            file_length = casanova.reader.count(file)
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                # Iterate over every tweet collected
                for row in tqdm(reader, total=file_length):
                    # Insert the tweet's user data
                    twitter_user_table.insert_values(
                        data=twitter_user_table.clean(data=row),
                        connection=connection,
                        on_conflict=twitter_user_table.on_conflict(),
                    )
                    # With the user inserted, insert the tweet data
                    tweet_table.insert_values(
                        data=tweet_table.clean(data=row),
                        connection=connection,
                        on_conflict=tweet_table.on_conflict(),
                    )
                    # With the tweet data inserted, establish a relationship between the tweet and search query
                    tweet_query_table.insert_values(
                        data=tweet_query_table.clean(data=row),
                        connection=connection,
                        on_conflict="DO NOTHING",
                    )


if __name__ == "__main__":
    main()
