from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

TWEET_TABLE_COLUMNS = [
    BaseColumn("id", DType.VAR20, DType.NOTNULL),
    BaseColumn("local_time", DType.DATETIME),
    BaseColumn("user_screen_name", DType.VAR250),
    BaseColumn("user_id", DType.VAR20, DType.NOTNULL),
    BaseColumn("text", DType.TEXT),
    BaseColumn("possibly_sensitive", DType.BOOL),
    BaseColumn("retweet_count", DType.BIGINT),
    BaseColumn("like_count", DType.BIGINT),
    BaseColumn("reply_count", DType.BIGINT),
    BaseColumn("impression_count", DType.BIGINT),
    BaseColumn("lang", DType.VAR20),
    BaseColumn("to_userid", DType.VAR20),
    BaseColumn("to_tweetid", DType.VAR20),
    BaseColumn("retweeted_id", DType.VAR20),
    BaseColumn("is_retweet", DType.BOOL),
    BaseColumn("retweeted_user_id", DType.VAR20),
    BaseColumn("retweeted_timestamp_utc", DType.DATETIME),
    BaseColumn("quoted_id", DType.VAR20),
    BaseColumn("is_quote_tweet", DType.BOOL),
    BaseColumn("quoted_user_id", DType.VAR20),
    BaseColumn("quoted_timestamp_utc", DType.DATETIME),
    BaseColumn("url", DType.VAR250),
    BaseColumn("place_country_code", DType.VAR20),
    BaseColumn("place_name", DType.TEXT),
    BaseColumn("place_type", DType.VAR20),
    BaseColumn("place_coordinates", DType.ARRAY),
    BaseColumn("links", DType.ARRAY),
    BaseColumn("domains", DType.ARRAY),
    BaseColumn("hashtags", DType.ARRAY),
    BaseColumn("media_urls", DType.ARRAY),
    BaseColumn("media_files", DType.ARRAY),
    BaseColumn("media_types", DType.ARRAY),
    BaseColumn("media_alt_texts", DType.ARRAY),
    BaseColumn("mentioned_names", DType.ARRAY),
    BaseColumn("mentioned_ids", DType.ARRAY),
    BaseColumn("collection_time", DType.DATETIME),
]


@dataclass
class TweetTable(BaseTable):
    """Dataclass holding information about the tweet table.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "tweet"
    columns = TWEET_TABLE_COLUMNS

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
