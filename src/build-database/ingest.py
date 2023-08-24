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
    type=click.Choice(["condor", "de facto", "science feedback"]),
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
    first and only positional argument of this command.
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
    if isinstance(connection, psycopg2_connection):
        new_table = None

        # Ingest original Condor dataset and enrich resources with titles
        if data_source == "condor":
            title_dataset = info["data sources"]["enriched titles"]
            new_table = ingestion_scripts.create_condor(
                connection=connection, dataset=file_path, enriched_titles=title_dataset
            )

        # Ingest original De Facto dataset and enrich resources with titles
        elif data_source == "de facto":
            title_dataset = info["data sources"]["enriched titles"]
            new_table = ingestion_scripts.create_de_facto(
                connection=connection, dataset=file_path, enriched_titles=title_dataset
            )

        # Ingest original Science Feedback and enrich resources with titles
        elif data_source == "science feedback":
            title_dataset = info["data sources"]["enriched titles"]
            new_table = ingestion_scripts.create_science(
                connection=connection, dataset=file_path, enriched_titles=title_dataset
            )

        # If a new table was successfully created, return a count of its rows
        if new_table:
            result = count_table_rows(connection=connection, table_name=new_table.name)
            print(f"\nThe program created table {new_table.name} with {result} rows.")


if __name__ == "__main__":
    cli()
