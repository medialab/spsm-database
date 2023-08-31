from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType


SEARCHABLE_TITLES_URLS_TABLE_COLUMNS = [
    BaseColumn("id", DType.SERIAL),
    BaseColumn("claim_id", DType.INT),
    BaseColumn("normalized_url", DType.TEXT),
    BaseColumn("tweet_search_url", DType.TEXT),
    BaseColumn("title_text", DType.TEXT),
    BaseColumn("tweet_search_title", DType.TEXT),
    BaseColumn("not_searched_on_twitter", DType.BOOL),
]


@dataclass
class SearchableTitlesURLSTable(BaseTable):
    """Dataclass holding information about the query dataset.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "searchable_titles_urls"
    columns = SEARCHABLE_TITLES_URLS_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
