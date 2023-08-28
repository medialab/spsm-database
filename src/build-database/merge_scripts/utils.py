from collections import namedtuple

Mapper = namedtuple(
    "Mapper",
    field_names=[
        "source_table_name",  # name of the table from which to select data
        "source_table_primary_key",
        "source_table_id",  # column name of the dataset's table id in the claims table
        "source_normalized_url",  # name of the dataset table's normalized URL column
        "source_normalized_url_hash",  # name of the dataset table's normalized URL hash column
        "source_first_fact_check",  # name of the dataset table's column for when the claim was fact-checked
        "source_universal_rating",  # name of the created column refering the dataset's fact check to an SPSM universal rating
    ],
    defaults=[None, None, None, None, None, None, None],
)
