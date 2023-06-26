# =============================================================================
# SPSM Create SQL Database
# =============================================================================
#
# Workflow for inserting Twitter data into SQL tables
#
import csv
import json

import casanova
from psycopg2.extensions import connection as psycopg2_connection
from tables.schemas import (
    CondorTable,
    ScienceFeedbackTable,
    DeFactoTable,
    URLTable,
)
from tqdm import tqdm
from connection.execute_query import execute_query


def insert_data_sources(connection: psycopg2_connection, data: dict):
    # Parse data file paths
    condor_file = data["condor"]
    science_file = data["science"]
    defacto_file = data["defacto"]

    # Instantiate the tables
    condor_table = CondorTable()
    science_table = ScienceFeedbackTable()
    defacto_table = DeFactoTable()
    tables = [condor_table, science_table, defacto_table]

    # (create and drop tables to clear database and start fresh)
    for table in tables:
        table.create(connection=connection)
    for table in tables:
        table.drop(connection=connection, force=True)

    # Create tables
    print("")
    for table in tables:
        print(f"(Re)creating table: {table.name}")
        table.create(connection=connection)

    print(
        f"\nImporting data from De Facto to table: {defacto_table.name}\n{defacto_file}"
    )
    with open(defacto_file, "r") as f:
        defacto_data = json.load(f)
        for clam_review in tqdm(defacto_data, total=len(defacto_data)):
            defacto_table.insert_values(
                data=defacto_table.clean(clam_review),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    print(f"\nImporting data from Condor to table: {condor_table.name}\n{condor_file}")
    file_length = casanova.reader.count(condor_file)
    with open(condor_file) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            condor_table.insert_values(
                data=condor_table.clean(data=row),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    print(
        f"\nImporting data from Science Feedback to table: {science_table.name}\n{science_file}"
    )
    with open(science_file, "r") as f:
        science_data = json.load(f)
        for clam_review in tqdm(science_data, total=len(science_data)):
            science_table.insert_values(
                data=science_table.clean(clam_review),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    print("\nCreating URL table")
    url_table = URLTable()

    # Clear out and set up URL table
    url_table.create(connection=connection)
    url_table.drop(connection=connection)
    url_table.create(connection=connection)

    # Insert normalized URL IDs from 3 data source tables
    url_table.add_url_ids(connection=connection)
