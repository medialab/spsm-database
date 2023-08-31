import csv

import casanova
import click
import yaml
from psycopg2.extensions import connection as psycopg2_connection
from tqdm import tqdm
from rich.progress import (
    Progress,
    TextColumn,
    SpinnerColumn,
    BarColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    MofNCompleteColumn,
)

from table_schemas.utils import clear_table
from tweet_scripts import tweet, tweet_claim, tweet_query
from utils import connect_to_database, count_table_rows
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

        # Insert data into the table via a join
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

    if isinstance(connection, psycopg2_connection):
        tweet_table = tweet.setup(connection=connection)
        tweet_query_table = tweet.setup(connection=connection)

        # ----------------------------- #
        # DEBUGGING
        if reset:
            clear_table(connection=connection, table=tweet_table)
        # ----------------------------- #

        with open(filepath_list, "r") as f, Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        ) as progress:
            Lines = f.readlines()
            global_task = progress.add_task(
                description="[bold yellow]Data files", total=len(Lines)
            )
            local_task = progress.add_task(
                description="[cyan]Tweets", start=False, visible=False
            )
            for n, line in enumerate(Lines):
                file = line.strip()
                print(f"\n[{n}] Counting data file length...")
                file_length = casanova.reader.count(file)
                progress.update(
                    task_id=local_task, total=file_length, completed=0, visible=True
                )
                print(f"    Importing Twitter data from file: {file}\n")
                with open(file, "r") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        tweet.insert(connection=connection, data=row)
                        tweet_query.insert(connection=connection, data=row)
                        progress.advance(task_id=local_task)
                # Update the progress bars
                progress.advance(task_id=global_task)


if __name__ == "__main__":
    cli()
