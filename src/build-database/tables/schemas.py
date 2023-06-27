# =============================================================================
# SPSM Database Tables
# =============================================================================
#
# Table schemas and cleaning methods
#
from dataclasses import dataclass

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


@dataclass
class CompletedURLDatasetTable(BaseTable):
    """Dataclass holding information about the condor data source.
    It possesses class methods to (1) parse a CSV (as dict) row and
    recast/clean the data.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    # (required) Name of the table
    name = "completed_urls_dataset"
    # (variable) All of the table's columns
    condor_url_rid = BaseColumn(name="condor_url_rid", type=VAR20)
    url_id = BaseColumn(name="url_id", type=VAR250)
    completed_url = BaseColumn(name="completed_url", type=TEXT)
    normalized_url = BaseColumn(name="normalized_url", type=TEXT)
    original_url_id = BaseColumn(name="original_url_id", type=VAR250)

    # (required) List of the columns
    columns = [
        condor_url_rid,
        url_id,
        completed_url,
        normalized_url,
        original_url_id,
    ]
    # (required) Primary key column name
    pk = f"{url_id.name}, {completed_url.name}"


@dataclass
class CompletedURLsTable(BaseTable):
    """Dataclass holding information about the condor data source.
    It possesses class methods to (1) parse a CSV (as dict) row and
    recast/clean the data.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    # (required) Name of the table
    name = "completed_urls"
    # (variable) All of the table's columns
    condor_table_id = BaseColumn(name="condor_table_id", type=INT)
    condor_url_rid = BaseColumn(name="condor_url_rid", type=VAR20)
    url_id = BaseColumn(name="url_id", type=VAR250)
    completed_url = BaseColumn(name="completed_url", type=TEXT)
    normalized_url = BaseColumn(name="normalized_url", type=TEXT)
    original_url_id = BaseColumn(name="original_url_id", type=VAR250)

    # (required) List of the columns
    columns = [
        url_id,
        condor_table_id,
        condor_url_rid,
        completed_url,
        normalized_url,
        original_url_id,
    ]
    # (required) Primary key column name
    pk = url_id.name


@dataclass
class CondorTable(BaseTable):
    """Dataclass holding information about the condor data source.
    It possesses class methods to (1) parse a CSV (as dict) row and
    recast/clean the data.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
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


@dataclass
class ScienceFeedbackTable(BaseTable):
    """Dataclass holding information about the science feedback data
    source. It possesses class methods to (1) parse a CSV (as dict)
    row and recast/clean the data.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
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


@dataclass
class DeFactoTable(BaseTable):
    """Dataclass holding information about the De Facto data source
    It possesses class methods to (1) parse a CSV (as dict) row.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
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


@dataclass
class URLTable(BaseTable):
    """Dataclass holding information about URLs.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    # (required) Name of the table
    name = "url"
    # (variable) All of the table's columns
    id = BaseColumn(name="id", type=VAR250, **{"null": NOTNULL})
    normalized_url = BaseColumn(name="normalized_url", type=TEXT, **{"null": NOTNULL})
    archive_url = BaseColumn(name="archive_url", type=TEXT)
    is_archived = BaseColumn(name="is_archived", type=TEXT)
    tweet_search_title = BaseColumn(name="tweet_search_title", type=TEXT)
    tweet_search_url = BaseColumn(name="tweet_search_url", type=TEXT)

    # (required) List of the columns
    columns = [
        id,
        normalized_url,
        archive_url,
        is_archived,
        tweet_search_title,
        tweet_search_url,
    ]
    # (required) Primary key column name
    pk = id.name
