from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType


TITLE_QUERIES_TABLE_COLUMNS = [
    BaseColumn("id", DType.SERIAL, DType.NOTNULL),
    BaseColumn("original_title", DType.TEXT),
    BaseColumn("tweet_search_title", DType.TEXT),
    BaseColumn("url_id", DType.VAR250),
    BaseColumn("manually_skipped", DType.BOOL),
    BaseColumn("same_as_original", DType.BOOL),
]


@dataclass
class TitleQueryDatasetTable(BaseTable):
    """Dataclass holding information about the title query dataset.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_title_query"
    columns = TITLE_QUERIES_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
