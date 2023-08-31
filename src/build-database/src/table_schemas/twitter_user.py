from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType


TWITTER_USER_TABLE_COLUMNS = [
    BaseColumn("id", DType.VAR20, DType.NOTNULL),
    BaseColumn("verified", DType.BOOL),
    BaseColumn("screen_name", DType.VAR250),
    BaseColumn("display_name", DType.VAR250),
    BaseColumn("description", DType.TEXT),
    BaseColumn("url", DType.VAR600),
    BaseColumn("image", DType.VAR600),
    BaseColumn("tweets", DType.BIGINT),
    BaseColumn("followers", DType.BIGINT),
    BaseColumn("friends", DType.BIGINT),
    BaseColumn("likes", DType.BIGINT),
    BaseColumn("lists", DType.BIGINT),
    BaseColumn("created_at", DType.DATETIME),
    BaseColumn("collection_time", DType.DATETIME),
]


@dataclass
class TwitterUserTable(BaseTable):
    """Dataclass holding information about the twitter_user table.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "twitter_user"
    columns = TWITTER_USER_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name

    @classmethod
    def on_conflict(cls) -> str:
        update_columns = [col.name for col in cls.columns if col.name != cls.pk]
        excluded_row = [f"EXCLUDED.{col}" for col in update_columns]
        # Update the row if the current colleciton time is older (greater) than the new collection time
        query = f"""
            DO UPDATE
            SET ({", ".join(update_columns)}) = ({", ".join(excluded_row)})
            WHERE ({cls.name}.collection_time) > EXCLUDED.collection_time
        """
        return query
