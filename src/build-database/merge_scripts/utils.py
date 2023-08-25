from collections import namedtuple

Mapper = namedtuple(
    "Mapper",
    field_names=[
        "source_table_name",  # name of the table from which to select data
        "source_table_primary_key",
        "source_table_id",  # column name of the dataset's table id in the claims table
        "source_normalized_url",  # name of the dataset table's normalized URL column
        "source_normalized_url_hash",  # name of the dataset table's normalized URL hash column
    ],
    defaults=[None, None, None, None, None],
)