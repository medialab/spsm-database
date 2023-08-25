from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

CLAIMS_TABLE_COLUMNS = [
    BaseColumn("id", DType.SERIAL, DType.NOTNULL),
    BaseColumn("condor_table_id", DType.INT),
    BaseColumn("de_facto_table_id", DType.TEXT),
    BaseColumn("science_feedback_table_id", DType.VAR20),
    BaseColumn("completed_url_table_id", DType.VAR250),
    BaseColumn("normalized_url", DType.TEXT),
    BaseColumn("normalized_url_hash", DType.VAR250),
    BaseColumn("archive_url", DType.TEXT),
    BaseColumn("title_from_html", DType.TEXT),
    BaseColumn("title_from_web_archive", DType.TEXT),
    BaseColumn("title_from_condor", DType.TEXT),
    BaseColumn("title_from_youtube", DType.TEXT),
    BaseColumn("universal_claim_rating", DType.INT),
    BaseColumn("inferred_language", DType.VAR20),
]


@dataclass
class ClaimsTable(BaseTable):
    """Dataclass holding information about the condor data source.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "claims"
    columns = CLAIMS_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
