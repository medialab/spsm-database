# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for inserting Twitter data into SQL tables
#
import csv

import casanova
from psycopg2.extensions import connection as psycopg2_connection
from tables.schemas import TweetQueryTable, TweetTable, TwitterUserTable, URLTable
from tqdm import tqdm
from parse_files.tweet import clean as tweet_clean
from parse_files.twitter_user import clean as user_clean


def insert_tweets(connection: psycopg2_connection, file: str):
    # Instantiate the tweet, user, and tweet-query relation tables
    tweet_table = TweetTable()
    tweet_query_table = TweetQueryTable()
    twitter_user_table = TwitterUserTable()
    url_table = URLTable()

    # Link the query table to the url table
    url_table.add_foreign_key(
        connection=connection,
        column=url_table.tweet_search_title.name,
        references=(tweet_query_table.name, tweet_query_table.query.name),
    )

    # Ingest data
    print(f"\nInserting data from: {file}")
    file_length = casanova.reader.count(file)
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        # Iterate over every tweet collected
        for row in tqdm(reader, total=file_length):
            # Insert the tweet's user data
            twitter_user_table.insert_values(
                data=user_clean(data=row),
                connection=connection,
                on_conflict=twitter_user_table.on_conflict(),
            )
            # With the user inserted, insert the tweet data
            tweet_table.insert_values(
                data=tweet_clean(data=row),
                connection=connection,
                on_conflict=tweet_table.on_conflict(),
            )
            # With the tweet data inserted, establish a relationship between the tweet and search query
            row = {"tweet_id": row["id"], "query": row["query"]}
            tweet_query_table.insert_values(
                data=row,
                connection=connection,
                on_conflict="DO NOTHING",
            )
