import casanova
import click
import yaml
from psycopg2.extensions import connection as Connection

from connection import connect_to_database
from csv_to_table_classes import TweetQueryTable, TweetTable, TwitterUserTable
from utils import ProgressBar, yield_csv_dict_row


@click.group()
def cli():
    pass


@cli.command("users")
@click.option("--config", type=click.STRING)
@click.option("--reset", is_flag=True, help="FOR TESTING ONLY: Drop existing tables")
@click.argument("filepath_list")
def users(config, reset, filepath_list):
    """
    Main function to manage insgestion of tweet-search result files.
    """
    with open(filepath_list) as f:
        filepaths = [f.strip() for f in f.readlines() if f != ""]

    with open(config, "r") as f:
        info = yaml.safe_load(f)
    connection = connect_to_database(yaml=info)

    if isinstance(connection, Connection):
        # Set up tables
        twitter_user_table = TwitterUserTable(connection=connection)
        twitter_user_table.create(reset)

        with ProgressBar() as progress:
            global_task = progress.add_task(
                description="[bold green]Processing result files",
                total=len(filepaths),
            )
            for n, file in enumerate(filepaths):
                print(f"\n[{n}] {file}")
                count_task = progress.add_task(
                    description="[bold yellow]Counting file length", total=1
                )
                file_length = casanova.count(file)
                progress.remove_task(count_task)

                local_task = progress.add_task(
                    description="[cyan]Importing rows", total=file_length
                )
                for row in yield_csv_dict_row(file=file):
                    try:
                        twitter_user_table.insert_row(row)
                    except Exception as e:
                        print(row)
                        raise e

                    # Update progress bars
                    progress.advance(local_task)
                progress.remove_task(local_task)
                progress.advance(global_task)

        print("\nFinished commiting queries.")

    else:
        print("\nDid not make any changes to database.")


@cli.command("tweets")
@click.option("--config", type=click.STRING)
@click.option("--reset", is_flag=True, help="FOR TESTING ONLY: Drop existing tables")
@click.argument("filepath_list")
def tweets(config, reset, filepath_list):
    """
    Main function to manage insgestion of tweet-search result files.
    """
    with open(filepath_list) as f:
        filepaths = [f.strip() for f in f.readlines() if f != ""]

    with open(config, "r") as f:
        info = yaml.safe_load(f)
    connection = connect_to_database(yaml=info)

    if isinstance(connection, Connection):
        # Set up tables
        tweet_table = TweetTable(connection=connection)
        tweet_table.create(reset)
        twitter_user_table = TwitterUserTable(connection=connection)
        twitter_user_table.create(reset)
        tweet_query_table = TweetQueryTable(connection=connection)
        tweet_query_table.create(reset)

        with ProgressBar() as progress:
            global_task = progress.add_task(
                description="[bold green]Processing result files",
                total=len(filepaths),
            )
            for n, file in enumerate(filepaths):
                print(f"\n[{n}] {file}")
                count_task = progress.add_task(
                    description="[bold yellow]Counting file length", total=1
                )
                file_length = casanova.count(file)
                progress.remove_task(count_task)

                local_task = progress.add_task(
                    description="[cyan]Importing rows", total=file_length
                )
                for row in yield_csv_dict_row(file=file):
                    tweet_table.insert_row(row)
                    twitter_user_table.insert_row(row)
                    tweet_query_table.insert_row(row)

                    # Update progress bars
                    progress.advance(local_task)
                progress.remove_task(local_task)
                progress.advance(global_task)

        print("\nFinished commiting queries.")

    else:
        print("\nDid not make any changes to database.")


if __name__ == "__main__":
    cli()
