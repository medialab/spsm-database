from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType


COMPLETED_URLS_DATASET_TABLE_COLUMNS = [
    BaseColumn("completed_normalized_url_hash", DType.VAR250),
    BaseColumn("completed_normalized_url", DType.TEXT),
    BaseColumn("hash_of_original_normalized_url", DType.VAR250),
    BaseColumn("condor_table_id", DType.INT),
    BaseColumn("condor_url_rid", DType.VAR20),
]


@dataclass
class CompletedURLDatasetTable(BaseTable):
    """Dataclass holding information about URLs from Condor
    that were augmented or "completed" to be more specific.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_completed_urls"
    columns = COMPLETED_URLS_DATASET_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "completed_normalized_url_hash")
        self.pk = pk_column.name
