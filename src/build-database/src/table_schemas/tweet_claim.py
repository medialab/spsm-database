from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType


TWEET_CLAIM_TABLE_COLUMNS = [
    BaseColumn("tweet_id", DType.VAR20),
    BaseColumn("claim_id", DType.INT),
    BaseColumn("search_type", DType.VAR250),
    BaseColumn("match_probability", DType.FLOAT),
]


@dataclass
class TweetClaimTable(BaseTable):
    """Dataclass holding information about the condor data source.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "tweet_claim"
    columns = TWEET_CLAIM_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        self.pk = "tweet_id, claim_id"
