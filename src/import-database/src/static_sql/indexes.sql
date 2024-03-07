--drop index if exists tweet_user_id_index ;


--create index tweet_user_id_index on tweet using hash (user_id) ;



drop index if exists tweet_retweeted_id_index ;


create index tweet_retweeted_id_index on tweet using hash (retweeted_id) ;


drop index if exists tweet_quoted_id_index ;


create index tweet_quoted_id_index on tweet using hash (quoted_id) ;


drop index if exists tweet_claim_search_by_title_index on tweet_claim using hash (search_by_title) ;
