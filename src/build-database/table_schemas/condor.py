from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

CONDOR_DATASET_TABLE_COLUMNS = [
    BaseColumn("id", DType.SERIAL, DType.NOTNULL),
    BaseColumn("condor_url_rid", DType.VAR20),
    BaseColumn("normalized_clean_url_hash", DType.VAR250),
    BaseColumn("normalized_clean_url", DType.TEXT),
    BaseColumn("clean_url", DType.TEXT),
    BaseColumn("first_post_time", DType.DATETIME),
    BaseColumn("share_title", DType.TEXT),
    BaseColumn("tpfc_rating", DType.TEXT),
    BaseColumn("tpfc_first_fact_check", DType.DATETIME),
    BaseColumn("public_shares_top_country", DType.VAR20),
    BaseColumn("normalized_fact_check_rating", DType.FLOAT),
]


@dataclass
class CondorDatasetTable(BaseTable):
    """Dataclass holding information about the condor data source.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_condor"
    columns = CONDOR_DATASET_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
