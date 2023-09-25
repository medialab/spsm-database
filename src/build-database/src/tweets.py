import csv

import casanova
import click
import yaml
from psycopg2.extensions import connection as psycopg2_connection
from rich.progress import (
    Progress,
    TextColumn,
    SpinnerColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)

from table_schemas.utils import clear_table
from tweet_scripts import tweet, tweet_claim, tweet_query
from utils import connect_to_database
from table_schemas.claims import ClaimsTable
from table_schemas.tweet_claim import TweetClaimTable
from table_schemas.tweet import TweetTable
from table_schemas.tweet_query import TweetQueryTable


@click.group()
def cli():
    pass


@cli.command("build-relations")
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
        # Relate Tweets to queries
        tweet_table = TweetTable()
        tweet_query_table = TweetQueryTable()
        tweet_query_table.add_foreign_key(
            foreign_key_column="tweet_id",
            target_table=tweet_table.name,
            target_table_primary_key=tweet_table.pk,
            connection=connection,
        )

        # Create the relational tweet-claim table
        tweet_claim_table = TweetClaimTable()
        clear_table(connection=connection, table=tweet_claim_table)

        # Insert data into the table
        tweet_claim.insert(connection=connection)

        # Establish foreign keys on the relational table
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


@cli.command("ingest-data")
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

    # Parse the paths of all the tweet files
    with open(filepath_list, "r") as f:
        filepaths = f.readlines()

    if isinstance(connection, psycopg2_connection):
        # If they don't exist, create the tables
        tweet_table = tweet.setup(connection=connection)
        tweet_query_table = tweet_query.setup(connection=connection)

        # ----------------------------- #
        # DEBUGGING
        if reset:
            clear_table(connection=connection, table=tweet_table)
        # ----------------------------- #

        # Set up the progress bar
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            TimeRemainingColumn(),
        ) as progress:
            global_ingestion_task = progress.add_task(
                description="[bold green]Processing data files", total=len(filepaths)
            )

            for pathname in filepaths:
                # Get name of file path and count length
                file = pathname.strip()
                count_task = progress.add_task(
                    description="[bold yellow]Counting file length", total=1
                )
                file_length = casanova.reader.count(file)
                progress.remove_task(count_task)

                # Import rows from CSV file
                local_ingestion_task = progress.add_task(
                    description="[cyan]Importing data", total=file_length
                )
                with open(file, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        tweet.insert(connection=connection, data=row)
                        tweet_query.insert(connection=connection, data=row)
                        progress.advance(local_ingestion_task)

                # Update global progress bar
                progress.remove_task(local_ingestion_task)
                progress.advance(task_id=global_ingestion_task)

        tweet_query_table.add_foreign_key(
            foreign_key_column="tweet_id",
            target_table=tweet_table.name,
            target_table_primary_key=tweet_table.pk,
            connection=connection,
        )


if __name__ == "__main__":
    cli()
