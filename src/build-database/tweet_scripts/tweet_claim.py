from psycopg2.extensions import connection as psycopg2_connection

from table_schemas.claims import ClaimsTable
from table_schemas.doc_title_relation import DocTitleRelationTable
from table_schemas.searchable_titles_urls import SearchableTitlesURLSTable
from table_schemas.tweet import TweetTable
from table_schemas.tweet_claim import TweetClaimTable
from table_schemas.tweet_query import TweetQueryTable
from table_schemas.utils import BaseTable
from utils import execute_query


def setup(connection: psycopg2_connection):
    table = TweetClaimTable()
    table.create(connection=connection)
    return table


def insert(connection: psycopg2_connection) -> BaseTable:
    tweet_claim = TweetClaimTable()
    tweet = TweetTable().name
    tweet_query = TweetQueryTable().name
    searchable_titles_urls = SearchableTitlesURLSTable().name
    doc_title_relation = DocTitleRelationTable().name
    claims = ClaimsTable().name
    query = f"""
INSERT INTO {tweet_claim.name} (claim_id, tweet_id)
select c.id as claim_id, t.id as tweet_id
from {tweet} t
join {tweet_query} tq on t.id = tq.tweet_id 
join {searchable_titles_urls} stu on stu.tweet_search_title = tq.query 
join {doc_title_relation} dtr on dtr.title_text = stu.title_text 
join {claims} c on dtr.claim_id = c.id 
on conflict do nothing
"""
    execute_query(connection=connection, query=query)
    return tweet_claim
