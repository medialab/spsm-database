from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

URL_ENRICHMENTS_TABLE_COLUMNS = [
    BaseColumn("id", DType.VAR250, DType.NOTNULL),
    BaseColumn("detected_language", DType.VAR20),
]


@dataclass
class URLEnrichmentsTable(BaseTable):
    """Dataclass holding information about URL enrichments.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "url_enrichments"
    columns = URL_ENRICHMENTS_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
