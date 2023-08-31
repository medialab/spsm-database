from psycopg2.extensions import connection as psycopg2_connection

from table_schemas.claims import ClaimsTable
from table_schemas.doc_title_relation import DocTitleRelationTable
from table_schemas.searchable_titles_urls import SearchableTitlesURLSTable
from table_schemas.tweet import TweetTable
from table_schemas.tweet_claim import TweetClaimTable
from table_schemas.tweet_query import TweetQueryTable
from table_schemas.utils import BaseTable
from utils import execute_query


def insert(connection: psycopg2_connection) -> BaseTable:
    # Get the names of the relevant tables
    tweet_claim = TweetClaimTable()
    tweet = TweetTable().name
    tweet_query = TweetQueryTable().name
    searchable_titles_urls = SearchableTitlesURLSTable().name
    doc_title_relation = DocTitleRelationTable().name
    claims = ClaimsTable().name

    # Compose and execute a query to insert relations via title
    query = f"""
INSERT INTO {tweet_claim.name} (claim_id, tweet_id, search_type)
SELECT c.id AS claim_id, t.id AS tweet_id, 'title'
FROM {tweet} t
JOIN {tweet_query} tq ON t.id = tq.tweet_id 
JOIN {searchable_titles_urls} stu ON stu.tweet_search_title = tq.query 
JOIN {doc_title_relation} dtr ON dtr.title_text = stu.title_text 
JOIN {claims} c ON dtr.claim_id = c.id 
ON CONFLICT DO NOTHING
"""
    execute_query(connection=connection, query=query)

    # Compose and execute a query to insert relations via URL
    query = f"""
INSERT INTO {tweet_claim.name} (claim_id, tweet_id, search_type)
SELECT c.id AS claim_id, t.id AS tweet_id, 'url'
FROM {tweet} t
JOIN {tweet_query} tq ON t.id = tq.tweet_id 
JOIN {searchable_titles_urls} stu ON stu.tweet_search_url = tq.query 
JOIN {doc_title_relation} dtr ON dtr.normalized_url = stu.normalized_url 
JOIN {claims} c ON dtr.claim_id = c.id 
ON CONFLICT DO NOTHING
"""
    execute_query(connection=connection, query=query)

    return tweet_claim
