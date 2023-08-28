import csv

import casanova
import click
import yaml
from psycopg2.extensions import connection as psycopg2_connection
from tqdm import tqdm

from table_schemas.utils import clear_table
from tweet_scripts import tweet, tweet_claim, tweet_query
from utils import connect_to_database, count_table_rows
from table_schemas.claims import ClaimsTable
from table_schemas.tweet_claim import TweetClaimTable
from table_schemas.tweet import TweetTable


@click.group()
def cli():
    pass


@cli.command("relation")
@click.option("--config", type=click.STRING)
def streamline(config):
    """
    Main function to streamline queries of Tweets and claims.
    """
    # Parse the configuration file
    with open(config, "r") as f:
        info = yaml.safe_load(f)

    print("\n================================")

    # Establish the PostgreSQL database connection
    connection = connect_to_database(yaml=info)

    if isinstance(connection, psycopg2_connection):
        tweet_claim_table = TweetClaimTable()
        tweet_table = TweetTable()
        clear_table(connection=connection, table=tweet_claim_table)
        tweet_claim.insert(connection=connection)

        claim_table = ClaimsTable()
        tweet_claim_table.add_foreign_key(
            foreign_key_column="claim_id",
            target_table=claim_table.name,
            target_table_primary_key=claim_table.pk,
            connection=connection,
        )
        tweet_claim_table.add_foreign_key(
            foreign_key_column="tweet_id",
            target_table=tweet_table.name,
            target_table_primary_key=tweet_table.pk,
            connection=connection,
        )


@cli.command("import")
@click.option("--config", type=click.STRING)
@click.option("--reset", is_flag=True, help="FOR TESTING ONLY: Drop existing tables")
@click.argument("filepath_list")
def insert(config, reset, filepath_list):
    """
    Main function to manage the ingestion of Tweets to the database.
    """
    # Parse the configuration file
    with open(config, "r") as f:
        info = yaml.safe_load(f)

    print("\n================================")

    # Establish the PostgreSQL database connection
    connection = connect_to_database(yaml=info)

    if isinstance(connection, psycopg2_connection):
        tweet_query_table = tweet_query.setup(connection=connection)
        tweet_table = tweet.setup(connection=connection)

        # ----------------------------- #
        # DEBUGGING
        if reset:
            clear_table(connection=connection, table=tweet_query_table)
            clear_table(connection=connection, table=tweet_table)
        # ----------------------------- #

        with open(filepath_list, "r") as f:
            Lines = f.readlines()
            for line in Lines:
                file = line.strip()
                print("\nCounting data file length...")
                file_length = casanova.reader.count(file)
                print(f"\nImporting Twitter data from file: {file}")
                with open(file, "r") as f:
                    reader = csv.DictReader(f)
                    for row in tqdm(reader, total=file_length):
                        tweet.insert(connection=connection, data=row)
                        tweet_query.insert(connection=connection, data=row)

                # After data has been ingested, add foreign key constraints
                tweet_query_table.add_foreign_key(
                    foreign_key_column="tweet_id",
                    target_table=tweet_table.name,
                    target_table_primary_key=tweet_table.pk,
                    connection=connection,
                )

                result = count_table_rows(
                    connection=connection, table_name=tweet_table.name
                )
                print(
                    f"\nThe program created table '{tweet_table.name}' with {result} rows."
                )
                print("\n================================")


if __name__ == "__main__":
    cli()
