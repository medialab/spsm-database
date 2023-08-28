from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

DEFACTO_DATASET_TABLE_COLUMNS = [
    BaseColumn("id", DType.TEXT, DType.NOTNULL),
    BaseColumn("normalized_claim_url_hash", DType.VAR250, DType.NOTNULL),
    BaseColumn("normalized_claim_url", DType.TEXT),
    BaseColumn("themes", DType.ARRAY),
    BaseColumn("tags", DType.ARRAY),
    BaseColumn("review_url", DType.TEXT),
    BaseColumn("review_publication_date", DType.DATETIME),
    BaseColumn("review_author", DType.TEXT),
    BaseColumn("claim", DType.TEXT),
    BaseColumn("claim_url", DType.TEXT),
    BaseColumn("claim_publication_date", DType.DATETIME),
    BaseColumn("claim_url_type", DType.TEXT),
    BaseColumn("claim_title", DType.TEXT),
    BaseColumn("claim_rating_value", DType.FLOAT),
    BaseColumn("claim_rating_name", DType.TEXT),
]


@dataclass
class DeFactoDatasetTable(BaseTable):
    """Dataclass holding information about the De Facto data source

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_de_facto"
    columns = DEFACTO_DATASET_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
