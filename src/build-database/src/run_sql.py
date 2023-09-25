import click
import yaml

from utils import connect_to_database, count_table_rows
import ingestion_scripts
from psycopg2.extensions import connection as psycopg2_connection
from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


@click.command()
@click.option("--config", type=click.STRING)
@click.argument("sql_file", type=click.STRING)
def cli(config, sql_file):
    # Parse the configuration file
    with open(config, "r") as f:
        info = yaml.safe_load(f)

    # Establish the PostgreSQL database connection
    connection = connect_to_database(yaml=info)

    # If the connection is good, proceed
    if isinstance(connection, psycopg2_connection):
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            TimeElapsedColumn(),
        ) as progress:
            print(f"Script: {sql_file}")
            progress.add_task(description=f"[bold green]Executing SQL")
            connection.autocommit = True
            cursor = connection.cursor()
            try:
                cursor.execute(open(sql_file, "r").read())
            except Exception as e:
                raise e

    else:
        if not sql_file:
            print(sql_file)
            raise FileNotFoundError
        if not connection:
            raise ConnectionError


if __name__ == "__main__":
    cli()
