from psycopg2.extensions import connection as psycopg2_connection

from table_schemas.tweet_query import TweetQueryTable


def setup(connection: psycopg2_connection):
    table = TweetQueryTable()
    table.create(connection=connection)
    return table


def clean(data: dict) -> dict:
    d = {"tweet_id": data["id"], "query": data["query"]}
    return d


def insert(connection: psycopg2_connection, data: dict):
    table = TweetQueryTable()
    data = clean(data)
    table.insert_values(data=data, connection=connection, on_conflict="DO NOTHING")
