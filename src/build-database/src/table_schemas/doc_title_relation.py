from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

DOC_TITLE_RELATION_TABLE_COLUMNS = [
    BaseColumn("id", DType.SERIAL),
    BaseColumn("claim_id", DType.INT),
    BaseColumn("normalized_url", DType.TEXT),
    BaseColumn("title_text", DType.TEXT),
    BaseColumn("title_type", DType.TEXT),
]


@dataclass
class DocTitleRelationTable(BaseTable):
    """Dataclass holding information about the condor data source.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "doc_title_relation"
    columns = DOC_TITLE_RELATION_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
