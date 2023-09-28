import click
import yaml

from utils import connect_to_database, count_table_rows
import ingestion_scripts
from psycopg2.extensions import connection as psycopg2_connection


@click.command()
@click.argument("config", type=click.STRING)
@click.option(
    "--data-source",
    prompt=True,
    type=click.Choice(
        [
            "condor",
            "de facto",
            "science feedback",
            "completed urls",
            "supplemental titles",
            "query titles",
            "query urls",
        ]
    ),
)
@click.option(
    "--no-prompt",
    is_flag=True,
    show_default=True,
    default=False,
    help="Skip the prompt that asks the user to double-check the path to the data file.",
)
def cli(config, data_source, no_prompt):
    """
    Main function to manage the ingestion of raw data to the database.
    Data can come from CSV files or JSON files. Paths to these files
    must be declared in the configuration YAML, which is this command's
    first and only positional argument.
    """
    # Parse the configuration file
    with open(config, "r") as f:
        info = yaml.safe_load(f)

    # Parse data source file path
    file_path = info["data sources"].get(data_source)

    if not no_prompt:
        print("\n--------------")
        click.echo(f"Ingesting data source {data_source.upper()} from file {file_path}")
        click.confirm(text="Is this ok?", abort=True)
        print("--------------\n")

    # Establish the PostgreSQL database connection
    connection = connect_to_database(yaml=info)

    # If the connection is good, proceed
    if isinstance(connection, psycopg2_connection) and file_path:
        new_table = None

        # Ingest original Condor dataset and enrich resources with titles
        if data_source == "condor":
            new_table = ingestion_scripts.create_condor(
                connection=connection,
                dataset=file_path,
            )

        # Ingest original De Facto dataset and enrich resources with titles
        elif data_source == "de facto":
            new_table = ingestion_scripts.create_de_facto(
                connection=connection,
                dataset=file_path,
            )

        # Ingest original Science Feedback and enrich resources with titles
        elif data_source == "science feedback":
            new_table = ingestion_scripts.create_science(
                connection=connection,
                dataset=file_path,
            )

        # Ingest the manually completed URLs
        elif data_source == "completed urls":
            new_table = ingestion_scripts.create_completed_urls(
                connection=connection, file=file_path
            )

        # Ingest the dataset that adds titles to data sources' URLs, aggregated
        elif data_source == "supplemental titles":
            new_table = ingestion_scripts.create_supplemental_titles_dataset_table(
                connection=connection, dataset=file_path
            )

        # Ingest the dataset that relates titles with searchable versions
        # and with a value indicating whether or not a search was attempted
        elif data_source == "query titles":
            new_table = ingestion_scripts.create_title_query_dataset_table(
                connection=connection, dataset=file_path
            )

        # Ingest the dataset that relates titles with searchable versions
        # and with a value indicating whether or not a search was attempted
        elif data_source == "query urls":
            new_table = ingestion_scripts.create_url_query_dataset_table(
                connection=connection, dataset=file_path
            )

        # If a new table was successfully created, return a count of its rows
        if new_table:
            result = count_table_rows(connection=connection, table_name=new_table.name)
            print(f"\nThe program created table {new_table.name} with {result} rows.")
            print("================================\n")

    else:
        if not file_path:
            print(file_path)
            raise FileNotFoundError
        if not connection:
            raise ConnectionError


if __name__ == "__main__":
    cli()
