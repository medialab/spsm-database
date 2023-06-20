# SQL Tables as classes
import ast
import re
from dataclasses import dataclass
from datetime import datetime

from tables.base_classes import BaseColumn, BaseTable

SERIAL = "SERIAL"
INT = "INT"
BIGINT = "BIGINT"
TEXT = "TEXT"
VAR20 = "VARCHAR(20)"
VAR250 = "VARCHAR(250)"
VAR600 = "VARCHAR(600)"
PRIMARY = "PRIMARY KEY"
NOTNULL = "NOT NULL"
DATETIME = "TIMESTAMP"
BOOL = "BOOLEAN"
ARRAY = "TEXT[]"


def clean_text(text: str | None) -> str | None:
    if text:
        return re.sub(
            pattern=r"'",
            repl="''",
            string=text,
        )


@dataclass
class TwitterUserTable(BaseTable):
    # (required) Name of the table
    name = "twitter_user"
    # (variable) All of the table's columns
    pid = BaseColumn(name="id", type=VAR20, **{"null": NOTNULL})
    verified = BaseColumn(name="verified", type=BOOL)
    screen_name = BaseColumn(name="screen_name", type=VAR250)
    display_name = BaseColumn(name="display_name", type=VAR250)
    description = BaseColumn(name="description", type=TEXT)
    url = BaseColumn(name="url", type=VAR600)
    image = BaseColumn(name="image", type=VAR600)
    tweets = BaseColumn(name="tweets", type=BIGINT)
    followers = BaseColumn(name="followers", type=BIGINT)
    friends = BaseColumn(name="friends", type=BIGINT)
    likes = BaseColumn(name="likes", type=BIGINT)
    lists = BaseColumn(name="lists", type=BIGINT)
    created_at = BaseColumn(name="created_at", type=DATETIME)
    collection_time = BaseColumn(name="collection_time", type=DATETIME)

    # (required) List of the columns
    columns = [
        pid,
        verified,
        screen_name,
        display_name,
        description,
        url,
        image,
        tweets,
        followers,
        friends,
        likes,
        lists,
        created_at,
        collection_time,
    ]
    # (required) Primary key column name
    pk = pid.name
    # (required) Addendum to be added to the end of the create command
    schema_addendum = [f"PRIMARY KEY({pk})"]

    @classmethod
    def clean(cls, data: dict) -> dict:
        # Select the user data fields from the CSV dict row
        selected_user_data = {}
        for k, v in data.items():
            if k in [f"user_{col.name}" for col in cls.columns]:
                k = k[5:]
                selected_user_data.update({k: v})
            elif k == "user_name":
                k = "display_name"
                selected_user_data.update({k: v})
            elif k == "collection_time":
                selected_user_data.update({k: v})
        # Clean the selected data fields
        for column in cls.columns:
            # Clean the text by replacing every single quote with 2 single quotes
            if column.type == TEXT or column.type.startswith("VAR"):
                selected_user_data.update(
                    {
                        column.name: clean_text(selected_user_data[column.name]),
                    }
                )
            # Cast integers as integers
            elif column.type == BIGINT:
                n = selected_user_data[column.name]
                try:
                    selected_user_data.update({column.name: int(n)})
                except Exception:
                    selected_user_data.update({column.name: 0})
            # Cast booleans as booleans
            if column.type == BOOL:
                b = selected_user_data[column.name]
                if b == "0":
                    selected_user_data.update({column.name: False})
                elif b == "1":
                    selected_user_data.update({column.name: True})
            if selected_user_data[column.name] == "":
                selected_user_data.update({column.name: None})
        return selected_user_data

    @classmethod
    def on_conflict(cls) -> str:
        update_columns = [col.name for col in cls.columns if col.name != cls.pk]
        excluded_row = [f"EXCLUDED.{col}" for col in update_columns]
        # Update the row if the current colleciton time is older (greater) than the new collection time
        query = f"""
            DO UPDATE
            SET ({", ".join(update_columns)}) = ({", ".join(excluded_row)})
            WHERE ({cls.name}.{cls.collection_time.name}) > EXCLUDED.{cls.collection_time.name}
        """
        return query


@dataclass
class TweetTable(BaseTable):
    # (required) Name of the table
    name = "tweet"
    # (variable) All of the table's columns
    pid = BaseColumn(name="id", type=VAR20, **{"null": NOTNULL})
    local_time = BaseColumn(name="local_time", type=DATETIME)
    user_screen_name = BaseColumn(name="user_screen_name", type=VAR250)
    user_id = BaseColumn(name="user_id", type=VAR20, **{"null": NOTNULL})
    text = BaseColumn(name="text", type=TEXT)
    possibly_sensitive = BaseColumn(name="possibly_sensitive", type=BOOL)
    retweet_count = BaseColumn(name="retweet_count", type=BIGINT)
    like_count = BaseColumn(name="like_count", type=BIGINT)
    reply_count = BaseColumn(name="reply_count", type=BIGINT)
    impression_count = BaseColumn(name="impression_count", type=BIGINT)
    lang = BaseColumn(name="lang", type=VAR20)
    to_userid = BaseColumn(name="to_userid", type=VAR20)
    to_tweetid = BaseColumn(name="to_tweetid", type=VAR20)
    retweeted_id = BaseColumn(name="retweeted_id", type=VAR20)
    is_retweet = BaseColumn(name="is_retweet", type=BOOL)
    retweeted_user_id = BaseColumn(name="retweeted_user_id", type=VAR20)
    retweeted_timestamp_utc = BaseColumn(name="retweeted_timestamp_utc", type=DATETIME)
    quoted_id = BaseColumn(name="quoted_id", type=VAR20)
    is_quote_tweet = BaseColumn(name="is_quote_tweet", type=BOOL)
    quoted_user_id = BaseColumn(name="quoted_user_id", type=VAR20)
    quoted_timestamp_utc = BaseColumn(name="quoted_timestamp_utc", type=DATETIME)
    url = BaseColumn(name="url", type=VAR250)
    place_country_code = BaseColumn(name="place_country_code", type=VAR20)
    place_name = BaseColumn(name="place_name", type=TEXT)
    place_type = BaseColumn(name="place_type", type=VAR20)
    place_coordinates = BaseColumn(name="place_coordinates", type=ARRAY)
    links = BaseColumn(name="links", type=ARRAY)
    domains = BaseColumn(name="domains", type=ARRAY)
    hashtags = BaseColumn(name="hashtags", type=ARRAY)
    media_urls = BaseColumn(name="media_urls", type=ARRAY)
    media_files = BaseColumn(name="media_files", type=ARRAY)
    media_types = BaseColumn(name="media_types", type=ARRAY)
    media_alt_texts = BaseColumn(name="media_alt_texts", type=ARRAY)
    mentioned_names = BaseColumn(name="mentioned_names", type=ARRAY)
    mentioned_ids = BaseColumn(name="mentioned_ids", type=ARRAY)
    collection_time = BaseColumn(name="collection_time", type=DATETIME)

    # (required) List of the columns
    columns = [
        pid,
        local_time,
        user_screen_name,
        user_id,
        text,
        possibly_sensitive,
        retweet_count,
        like_count,
        reply_count,
        impression_count,
        lang,
        to_userid,
        to_tweetid,
        retweeted_id,
        is_retweet,
        retweeted_user_id,
        retweeted_timestamp_utc,
        quoted_id,
        is_quote_tweet,
        quoted_user_id,
        quoted_timestamp_utc,
        url,
        place_country_code,
        place_name,
        place_type,
        place_coordinates,
        links,
        domains,
        hashtags,
        media_urls,
        media_files,
        media_types,
        media_alt_texts,
        mentioned_names,
        mentioned_ids,
        collection_time,
    ]
    # (required) Primary key column name
    pk = pid.name
    # (required) Addendum to be added to the end of the create command
    schema_addendum = [
        f"PRIMARY KEY({pk})",
        f"FOREIGN KEY({user_id.name}) REFERENCES twitter_user(id)",
    ]

    @classmethod
    def clean(cls, data: dict) -> dict:
        # Select the tweet data fields from the CSV dict row
        selected_tweet_data = {
            k: v for k, v in data.items() if k in [col.name for col in cls.columns]
        }
        additional_fields = [cls.is_quote_tweet, cls.is_retweet]
        for field in additional_fields:
            selected_tweet_data.update({field.name: None})
        # Clean the select data fields
        for column in cls.columns:
            # Clean up empty strings with null value
            if selected_tweet_data[column.name] == "":
                selected_tweet_data.update({column.name: None})
            # Clean the text by replacing every single quote with 2 single quotes
            if column.type == TEXT or column.type.startswith("VAR"):
                selected_tweet_data.update(
                    {
                        column.name: clean_text(selected_tweet_data[column.name]),
                    }
                )
            # Clean boolean fields
            if column.type == BOOL:
                if selected_tweet_data[column.name] == "1":
                    selected_tweet_data.update({column.name: True})
                else:
                    selected_tweet_data.update({column.name: False})
            # Parse timestamp integer
            if column.name.endswith("timestamp_utc") and column.type == DATETIME:
                s = None
                try:
                    s = str(
                        datetime.fromtimestamp(int(selected_tweet_data[column.name]))
                    )
                except TypeError:
                    pass
                selected_tweet_data.update({column.name: s})
            # Parse array data
            elif column.type == ARRAY:
                parsed_column = selected_tweet_data[column.name]
                array = ""
                # If the data is written as a list (i.e. coordinates), read it literally
                if (
                    parsed_column
                    and parsed_column.startswith("[")
                    and parsed_column.endswith("]")
                ):
                    try:
                        array = ast.literal_eval(parsed_column)
                    except Exception:
                        pass
                # Otherwise, try to unnest the data on the | delimiter
                elif parsed_column:
                    array = parsed_column.split("|")
                # Wrap the array values in double quotes and flatten to a string
                if len(array) > 0:
                    array = ", ".join([f'"{v}"' for v in array if v])
                # Wrap curly brackets around the double-quoted array string
                selected_tweet_data.update({column.name: "{" + str(array) + "}"})
            # Create additional "is retweet" column
            elif column.name == "is_retweet":
                if selected_tweet_data["retweeted_id"]:
                    selected_tweet_data.update({column.name: True})
                else:
                    selected_tweet_data.update({column.name: False})
            # Create additional "is quote tweet" column
            elif column.name == "is_quote_tweet":
                if selected_tweet_data["quoted_id"]:
                    selected_tweet_data.update({column.name: True})
                else:
                    selected_tweet_data.update({column.name: False})
        return selected_tweet_data

    @classmethod
    def on_conflict(cls) -> str:
        update_columns = [col.name for col in cls.columns if col.name != cls.pk]
        excluded_row = [f"EXCLUDED.{col}" for col in update_columns]
        # Update the row if the current colleciton time is older (greater) than the new collection time
        query = f"""
            DO UPDATE
            SET ({", ".join(update_columns)}) = ({", ".join(excluded_row)})
            WHERE ({cls.name}.{cls.collection_time.name}) > EXCLUDED.{cls.collection_time.name}
        """
        return query


@dataclass
class TweetQueryTable(BaseTable):
    # (required) Name of the table
    name = "tweet_query"
    # (variable) All of the table's columns
    tweet_id = BaseColumn(name="tweet_id", type=VAR20, **{"null": NOTNULL})
    query = BaseColumn(name="query", type=TEXT, **{"null": NOTNULL})

    # (required) List of the columns
    columns = [tweet_id, query]
    # (required) Primary key column name
    pk = f"{tweet_id.name}, {query.name}"
    # (required) Addendum to be added to the end of the create command
    schema_addendum = [
        f"CONSTRAINT pk PRIMARY KEY ({pk})",
        f"FOREIGN KEY({tweet_id.name}) REFERENCES tweet(id)",
    ]

    @classmethod
    def clean(cls, data: dict) -> dict:
        clean_search_query = re.sub(pattern=r"'", repl="''", string=data["query"])
        return {
            "tweet_id": data["id"],
            "query": clean_search_query,
        }
