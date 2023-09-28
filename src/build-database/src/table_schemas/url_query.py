from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType


URL_QUERIES_TABLE_COLUMNS = [
    BaseColumn("url_id", DType.VAR250, DType.NOTNULL),
    BaseColumn("normalized_url", DType.TEXT),
    BaseColumn("tweet_search_url", DType.TEXT),
    BaseColumn("manually_skipped", DType.BOOL),
]


@dataclass
class URLQueryDatasetTable(BaseTable):
    """Dataclass holding information about the URL query dataset.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_url_query"
    columns = URL_QUERIES_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "url_id")
        self.pk = pk_column.name
