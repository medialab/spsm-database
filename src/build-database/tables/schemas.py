# =============================================================================
# SPSM Database Tables
# =============================================================================
#
# Table schemas and cleaning methods
#
import ast
import re
from dataclasses import dataclass
from datetime import datetime

from tables.base_classes import BaseColumn, BaseTable, execute_query

# To help prevent spelling errors,
# constants of SQL data types
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
FLOAT = "FLOAT"


@dataclass
class TwitterUserTable(BaseTable):
    """Dataclass holding information about the twitter_user table.
    It possesses class methods to (1) parse a CSV (as dict) row and
    recast/clean the data, and (2) compose a string that says what
    to do if there is a conflict on the table's constraints.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    - schema_addendum (list[str]) : Array of additional instructions
        to be used when creating the table schema
    """

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
        """Parse user fields from a CSV (as dict) row and recast/clean the data.

        Param:
        data (dict): CSV row as a dictionary

        Return:
        selected_user_data (dict): Key-value pairs of column names and values
        """
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
            if selected_user_data[column.name] == "":
                selected_user_data.update({column.name: None})
            # Cast booleans as booleans
            if column.type == BOOL:
                b = selected_user_data[column.name]
                if b == "0":
                    selected_user_data.update({column.name: False})
                elif b == "1":
                    selected_user_data.update({column.name: True})
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
    """Dataclass holding information about the tweet table.
    It possesses class methods to (1) parse a CSV (as dict) row and
    recast/clean the data, and (2) compose a string that says what
    to do if there is a conflict on the table's constraints.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    - schema_addendum (list[str]) : Array of additional instructions
        to be used when creating the table schema
    """

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
        """Parse tweet fields from a CSV (as dict) row and recast/clean the data.

        Param:
        data (dict): CSV row as a dictionary

        Return:
        selected_tweet_data (dict): Key-value pairs of column names and values
        """
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
            # Clean boolean fields
            if column.type == BOOL:
                if selected_tweet_data[column.name] == "1":
                    selected_tweet_data.update({column.name: True})
                else:
                    selected_tweet_data.update({column.name: False})
            # Parse timestamp integer
            elif column.name.endswith("timestamp_utc") and column.type == DATETIME:
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
                else:
                    array = None
                selected_tweet_data.update({column.name: array})
            # Create additional "is retweet" column
            if column.name == "is_retweet":
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
    """Dataclass holding information about the tweet_query table.
    It possesses class methods to (1) parse a CSV (as dict) row and
    recast/clean the data.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    - schema_addendum (list[str]) : Array of additional instructions
        to be used when creating the table schema
    """

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
        """Parse a CSV (as dict) row and clean the text data.
        Param:
        data (dict): CSV row as a dictionary

        Return:
        (dict): Key-value pairs of column names and values
        """
        clean_search_query = re.sub(pattern=r"'", repl="''", string=data["query"])
        return {
            "tweet_id": data["id"],
            "query": clean_search_query,
        }


@dataclass
class CondorTable(BaseTable):
    """Dataclass holding information about the condor data source.
    It possesses class methods to (1) parse a CSV (as dict) row and
    recast/clean the data.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    - schema_addendum (list[str]) : Array of additional instructions
        to be used when creating the table schema
    """

    # (required) Name of the table
    name = "condor"
    # (variable) All of the table's columns
    id = BaseColumn(name="id", type=SERIAL, **{"null": NOTNULL})
    condor_url_rid = BaseColumn(name="condor_url_rid", type=VAR20)
    url_id = BaseColumn(name="url_id", type=VAR250)
    normalized_url = BaseColumn(name="normalized_url", type=TEXT)
    clean_url = BaseColumn(name="clean_url", type=TEXT)
    first_post_time = BaseColumn(name="first_post_time", type=DATETIME)
    share_title = BaseColumn(name="share_title", type=TEXT)
    tpfc_rating = BaseColumn(name="tpfc_rating", type=TEXT)
    tpfc_first_fact_check = BaseColumn(name="tpfc_first_fact_check", type=DATETIME)
    public_shares_top_country = BaseColumn(name="public_shares_top_country", type=VAR20)

    # (required) List of the columns
    columns = [
        id,
        condor_url_rid,
        url_id,
        normalized_url,
        clean_url,
        first_post_time,
        share_title,
        tpfc_rating,
        tpfc_first_fact_check,
        public_shares_top_country,
    ]
    # (required) Primary key column name
    pk = id.name
    # (required) Addendum to be added to the end of the create command
    schema_addendum = [f"PRIMARY KEY({pk})"]

    @classmethod
    def clean(cls, data: dict) -> dict:
        condor_id = data.pop("url_rid")
        url_id = data.pop("hash")
        data.update({"condor_url_rid": condor_id, "url_id": url_id})
        for k, v in data.items():
            if v == "":
                data.update({k: None})
        return data


@dataclass
class ScienceFeedbackTable(BaseTable):
    """Dataclass holding information about the science feedback data
    source. It possesses class methods to (1) parse a CSV (as dict)
    row and recast/clean the data.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    - schema_addendum (list[str]) : Array of additional instructions
        to be used when creating the table schema
    """

    # (required) Name of the table
    name = "science_feedback"
    # (variable) All of the table's columns
    id = BaseColumn(name="id", type=VAR20, **{"null": NOTNULL})
    url_id = BaseColumn(name="url_id", type=VAR250, **{"null": NOTNULL})
    url_content_id = BaseColumn(name="url_content_id", type=VAR20, **{"null": NOTNULL})
    claim_reviewed = BaseColumn(name="claim_reviewed", type=TEXT)
    published_date = BaseColumn(name="published_date", type=DATETIME)
    publisher = BaseColumn(name="publisher", type=TEXT)
    review_author = BaseColumn(name="review_author", type=TEXT)
    review_rating_value = BaseColumn(name="review_rating_value", type=FLOAT)
    review_rating_standard_form = BaseColumn(
        name="review_rating_standard_form", type=TEXT
    )
    url = BaseColumn(name="url", type=TEXT)
    normalized_url = BaseColumn(name="normalized_url", type=TEXT)
    url_rating_name = BaseColumn(name="url_rating_name", type=TEXT)
    url_rating_value = BaseColumn(name="url_rating_value", type=FLOAT)
    updated_date = BaseColumn(name="updated_date", type=DATETIME)
    review_url = BaseColumn(name="review_url", type=TEXT)

    # (required) List of the columns
    columns = [
        id,
        url_id,
        url_content_id,
        claim_reviewed,
        published_date,
        publisher,
        review_author,
        review_rating_value,
        review_rating_standard_form,
        url,
        normalized_url,
        url_rating_name,
        url_rating_value,
        updated_date,
        review_url,
    ]
    # (required) Primary key column name
    pk = id.name
    # (required) Addendum to be added to the end of the create command
    schema_addendum = [f"PRIMARY KEY({pk})"]

    @classmethod
    def clean(cls, data: dict) -> dict:
        full_data = {}
        flattened = data["flattened_metadata"]
        # Simplify some field names and remove CamelCase
        standard_metadata = {
            "id": flattened["id"],
            "url_id": flattened["hash"],
            "url_content_id": flattened["urlContentId"],
            "claim_reviewed": flattened["claimReviewed"],
            "published_date": flattened["publishedDate"],
            "publisher": flattened["publisher"],
            "review_author": flattened["reviews_author"],
            "review_rating_value": flattened["reviews_reviewRatings_ratingValue"],
            "review_rating_standard_form": flattened[
                "reviews_reviewRatings_standardForm"
            ],
            "url": flattened["url"],
            "normalized_url": flattened["normalized_url"],
            "url_rating_name": flattened["urlReviews_reviewRatings_alternateName"],
            "url_rating_value": flattened["urlReviews_reviewRatings_ratingValue"],
        }
        for k, v in standard_metadata.items():
            if v == "":
                full_data.update({k: None})
            else:
                full_data.update({k: v})
        # When available, add data not in the original CSV
        review_url = (None,)
        if isinstance(data.get("reviews"), list) and len(data["reviews"]) > 0:
            review_url = data["reviews"][0].get("reviewUrl")
        full_data.update(
            {"updated_date": data.get("updatedDate"), "review_url": review_url}
        )
        return full_data


@dataclass
class DeFactoTable(BaseTable):
    """Dataclass holding information about the De Facto data source
    It possesses class methods to (1) parse a CSV (as dict) row.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    - schema_addendum (list[str]) : Array of additional instructions
        to be used when creating the table schema
    """

    # (required) Name of the table
    name = "de_facto"
    # (variable) All of the table's columns
    id = BaseColumn(name="id", type=TEXT, **{"null": NOTNULL})
    url_id = BaseColumn(name="url_id", type=VAR250, **{"null": NOTNULL})
    normalized_url = BaseColumn(name="normalized_url", type=TEXT)
    themes = BaseColumn(name="themes", type=ARRAY)
    tags = BaseColumn(name="tags", type=ARRAY)
    review_url = BaseColumn(name="review_url", type=TEXT)
    review_publication_date = BaseColumn(name="review_publication_date", type=DATETIME)
    review_author = BaseColumn(name="review_author", type=TEXT)
    claim = BaseColumn(name="claim", type=TEXT)
    claim_url = BaseColumn(name="claim_url", type=TEXT)
    claim_publication_date = BaseColumn(name="claim_publication_date", type=DATETIME)
    claim_url_type = BaseColumn(name="claim_url_type", type=TEXT)
    claim_title = BaseColumn(name="claim_title", type=TEXT)
    claim_rating_value = BaseColumn(name="claim_rating_value", type=INT)
    claim_rating_name = BaseColumn(name="claim_rating_name", type=TEXT)

    # (required) List of the columns
    columns = [
        id,
        url_id,
        normalized_url,
        themes,
        tags,
        review_url,
        review_publication_date,
        review_author,
        claim,
        claim_url,
        claim_publication_date,
        claim_url_type,
        claim_title,
        claim_rating_value,
        claim_rating_name,
    ]
    # (required) Primary key column name
    pk = id.name
    # (required) Addendum to be added to the end of the create command
    schema_addendum = [f"PRIMARY KEY({pk})"]

    @classmethod
    def clean(cls, data: dict) -> dict:
        flattened_metadata = data["flattened_metadata"]
        claimreview = data["claim-review"]
        full_data = {
            "id": data["id"],
            "url_id": flattened_metadata["hash"],
            "normalized_url": flattened_metadata["normalized_url"],
            "themes": data["themes"],
            "tags": data["tags"],
            "review_url": data["claim-review"]["url"],
            "review_publication_date": claimreview["datePublished"],
            "review_author": claimreview["author"].get("name"),
            "claim": flattened_metadata["claim-review_claimReviewed"],
            "claim_url": flattened_metadata["claim-review_itemReviewed_appearance_url"],
            "claim_publication_date": flattened_metadata[
                "claim-review_itemReviewed_datePublished"
            ],
            "claim_url_type": claimreview["itemReviewed"]["appearance"].get("@type"),
            "claim_title": claimreview["itemReviewed"]["appearance"]["headline"],
            "claim_rating_value": flattened_metadata[
                "claim-review_reviewRating_ratingValue"
            ],
            "claim_rating_name": flattened_metadata[
                "claim-review_reviewRating_alternateName"
            ],
        }
        for k, v in full_data.items():
            if v == "":
                v = None
            full_data.update({k: v})
        return full_data


@dataclass
class URLTable(BaseTable):
    """Dataclass holding information about URLs.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    - schema_addendum (list[str]) : Array of additional instructions
        to be used when creating the table schema
    """

    # (required) Name of the table
    name = "normalized_url"
    # (variable) All of the table's columns
    id = BaseColumn(name="id", type=VAR250, **{"null": NOTNULL})
    normalized_url_id = BaseColumn(
        name="normalized_url_id", type=VAR250, **{"null": NOTNULL}
    )
    normalized_url = BaseColumn(name="normalized_url", type=TEXT, **{"null": NOTNULL})
    archive_url = BaseColumn(name="archive_url", type=TEXT)
    is_archived = BaseColumn(name="is_archived", type=TEXT)

    # (required) List of the columns
    columns = [id, normalized_url_id, normalized_url, archive_url, is_archived]
    # (required) Primary key column name
    pk = id.name
    # (required) Addendum to be added to the end of the create command
    schema_addendum = [f"PRIMARY KEY({pk})"]

    @classmethod
    def add_url_ids(cls, connection):
        tables = ["de_facto", "science_feedback", "condor"]

        def insert(table_name):
            query = f"""
            INSERT INTO {cls.name}
            SELECT url_id AS normalized_url_id, url_id AS id, normalized_url
            FROM {table_name}
            GROUP BY url_id, normalized_url
            ON CONFLICT (id) DO NOTHING
            """
            execute_query(connection=connection, query=query)

        def add_foreign_key(table_name):
            query = f"""
            ALTER TABLE {table_name} ADD FOREIGN KEY (url_id) REFERENCES {cls.name} ({cls.id.name})
            """
            execute_query(connection=connection, query=query)

        for table in tables:
            insert(table_name=table)
            add_foreign_key(table_name=table)
