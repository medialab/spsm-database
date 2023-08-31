import ast
from datetime import datetime

from psycopg2.extensions import connection as psycopg2_connection

from table_schemas.tweet import TweetTable
from table_schemas.utils import DType, BaseTable


def setup(connection: psycopg2_connection):
    table = TweetTable()
    table.create(connection=connection)
    return table


def clean(data: dict) -> dict:
    table = TweetTable()

    # Remove key-value pairs from the row if the key is not in the table
    table_cols = [col.name for col in table.columns]
    data = {k: v for k, v in data.items() if k in table_cols}

    array_cols = [col.name for col in table.columns if col.type == DType.ARRAY]
    bool_cols = [col.name for col in table.columns if col.type == DType.BOOL]
    d = {}
    for k, v in data.items():
        # Cast parsed empty string to None
        if v == "":
            v = None

        # Cast parsed string to boolean
        if k in bool_cols and v:
            if v == "1":
                v = True
            else:
                v = False

        # Cast parsed string to array
        if k in array_cols and isinstance(v, str):
            array = None
            # If the data is written as a list (i.e. coordinates), read it literally
            if v.startswith("[") and v.endswith("]"):
                try:
                    array = ast.literal_eval(v)
                except Exception:
                    pass
                # Otherwise, try to unnest the data on the | delimiter
                array = v.split("|")
            v = array

        # Parse timestamp integer
        if k.endswith("timestamp_utc") and v:
            try:
                s = str(datetime.fromtimestamp(int(v)))
                v = s
            except TypeError:
                v = None

        # Create "is_retweet" field
        if k == "retweeted_id":
            if v:
                d.update({"is_retweet": True})
            else:
                d.update({"is_retweet": False})

        # Create "is_quote_tweet" field
        if k == "quoted_id":
            if v:
                d.update({"is_quote_tweet": True})
            else:
                d.update({"is_quote_tweet": False})

        d.update({k: v})

    return d


def on_conflict() -> str:
    table = TweetTable()
    update_columns = [col.name for col in table.columns if col.name != table.pk]
    excluded_row = [f"EXCLUDED.{col}" for col in update_columns]
    # Update the row if the current colleciton time is older (greater) than the new collection time
    query = f"""
        DO UPDATE
        SET ({", ".join(update_columns)}) = ({", ".join(excluded_row)})
        WHERE ({table.name}.collection_time) > EXCLUDED.collection_time
    """
    return query


def insert(connection: psycopg2_connection, data: dict) -> BaseTable:
    table = TweetTable()
    data = clean(data)
    table.insert_values(data=data, connection=connection, on_conflict=on_conflict())
    return table
