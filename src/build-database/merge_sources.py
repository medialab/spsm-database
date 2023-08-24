import click
import yaml
from psycopg2.extensions import connection as psycopg2_connection

from table_schemas.claims import ClaimsTable
from table_schemas.condor import CondorDatasetTable
from table_schemas.de_facto import DeFactoDatasetTable
from table_schemas.science import ScienceFeedbackDatasetTable
from table_schemas.utils import clear_table
from utils import connect_to_database


@click.command()
@click.argument("config")
def main(config):
    # Connect to the database
    with open(config, "r") as f:
        info = yaml.safe_load(f)
    connection = connect_to_database(info)

    if isinstance(connection, psycopg2_connection):
        # Initialize Claims table
        target_table = ClaimsTable()
        clear_table(connection=connection, table=target_table)

        sources = [
            CondorDatasetTable(),
            DeFactoDatasetTable(),
            ScienceFeedbackDatasetTable(),
        ]


if __name__ == "__main__":
    main()
