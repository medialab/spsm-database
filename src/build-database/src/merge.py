import click
import yaml
from psycopg2.extensions import connection as psycopg2_connection

from merge_scripts.claims import create_claims_table
from merge_scripts.doc_title_rel import create_doc_title_relation_table
from merge_scripts.unique_urls import create_url_enrichment_table
from utils import connect_to_database, count_table_rows


@click.command()
@click.argument("config")
def main(config):
    """
    Main function to manage the merging of all the datasets into a
    central claims table and then to explode those claims into a
    relational table that records each assoction between a document
    (URL) and a title attributed to that document. A document in the
    claims table could have a title from Condor, YouTube, its HTML,
    or Web Archive.

    As its first and only positional argument, this command requires
    the path to a configuration YAML which contains details about the
    PostgreSQL connection.
    """
    # Connect to the database
    with open(config, "r") as f:
        info = yaml.safe_load(f)
    connection = connect_to_database(info)

    if isinstance(connection, psycopg2_connection):
        # Create the claims table by merging from dataset tables
        claims_table = create_claims_table(connection=connection)
        result = count_table_rows(connection=connection, table_name=claims_table.name)
        print(f"\nThe program created table {claims_table.name} with {result} rows.")

        # Create the relational table between a document (URL) and its titles
        relational_table = create_doc_title_relation_table(connection=connection)
        result = count_table_rows(
            connection=connection, table_name=relational_table.name
        )
        print(
            f"\nThe program created table {relational_table.name} with {result} rows."
        )

        # Create a de-duplicated table of all URLs, in which to store enrichments
        url_enrichment_table = create_url_enrichment_table(connection=connection)
        result = count_table_rows(
            connection=connection, table_name=url_enrichment_table.name
        )
        print(
            f"\nThe program created table {url_enrichment_table.name} with {result} rows."
        )


if __name__ == "__main__":
    main()
