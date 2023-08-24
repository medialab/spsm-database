import csv
from dataclasses import dataclass

import casanova
from psycopg2.extensions import connection
from tqdm import tqdm

from table_schemas.utils import (
    BaseColumn,
    BaseTable,
    DType,
    basic_csv_row_cleaning,
    clear_table,
)
from utils import execute_query

ENRICHED_TITLE_DATASET_TABLE_COLUMNS = [
    BaseColumn("url_id", DType.VAR250, DType.NOTNULL),
    BaseColumn("normalized_url", DType.TEXT),
    BaseColumn("archive_url", DType.TEXT),
    BaseColumn("condor_share_title", DType.TEXT),
    BaseColumn("yt_video_headline", DType.TEXT),
    BaseColumn("webpage_title", DType.TEXT),
    BaseColumn("webarchive_search_title", DType.TEXT),
]


@dataclass
class EnrichedTitleDatasetTable(BaseTable):
    """Dataclass holding information about the condor data source.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_enriched_titles"
    columns = ENRICHED_TITLE_DATASET_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "url_id")
        self.pk = pk_column.name


def setup_enriched_title_dataset_table(connection: connection, dataset: str):
    title_table = EnrichedTitleDatasetTable()
    print(f"Creating data of enriched titles in table {title_table.name}")
    clear_table(connection=connection, table=title_table)
    file_length = casanova.reader.count(dataset)
    with open(dataset) as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, total=file_length):
            row.pop("sources")
            data = basic_csv_row_cleaning(row)
            title_table.insert_values(
                data=data,
                connection=connection,
                on_conflict="DO NOTHING",
            )


def add_enriched_titles(
    connection: connection, target_url_id_col_name: str, target_table: BaseTable
):
    title_table = EnrichedTitleDatasetTable()

    title_columns = [
        ("webpage_title", "title_from_html"),
        ("webarchive_search_title", "title_from_web_archive"),
        ("yt_video_headline", "title_from_youtube"),
    ]
    # To target table, add new columns in which to store titles
    for _, new_col in title_columns:
        query = f"""
        ALTER TABLE {target_table.name}
        ADD COLUMN IF NOT EXISTS {new_col} TEXT
        """
        execute_query(connection=connection, query=query)

    # While joining target table and enriched titles table,
    # update the new columns with corresponding data
    for enriched_title_col, new_col in title_columns:
        query = f"""
        UPDATE {target_table.name}
        SET {new_col} = {title_table.name}.{enriched_title_col}
        FROM {title_table.name}
        WHERE {title_table.name}.url_id = {target_table.name}.{target_url_id_col_name}
        """
        execute_query(connection=connection, query=query)
