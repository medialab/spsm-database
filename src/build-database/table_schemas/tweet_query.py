from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

TWEET_QUERY_TABLE_COLUMNS = [
    BaseColumn("tweet_id", DType.VAR20, DType.NOTNULL),
    BaseColumn("query", DType.TEXT, DType.NOTNULL),
]


@dataclass
class TweetQueryTable(BaseTable):
    """Dataclass holding information about the tweet_query table.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "tweet_query"
    columns = TWEET_QUERY_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        self.pk = "tweet_id, query"
