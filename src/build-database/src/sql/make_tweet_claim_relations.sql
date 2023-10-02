drop table if exists tweet_claim cascade ;


create table tweet_claim (id serial primary key, tweet_id varchar(20), claim_id integer, search_by_title boolean, query_validity float, validity_justification text, match_probability float) ;


alter table tweet_claim add constraint claim_fk
foreign key (claim_id) references claims (id) ;


alter table tweet_claim add constraint tweet_fk
foreign key (tweet_id) references tweet (id) ;

/* Insert tweet-claim reltions for searches by title */
insert into tweet_claim (tweet_id, claim_id, search_by_title, query_validity, validity_justification, match_probability)
select tq.tweet_id,
       c.id,
       TRUE,
       dtq.validity,
       dtq.validity_justification,
       0.5
from tweet_query tq
join dataset_title_query dtq on tq.query = dtq.tweet_search_title
join claim_titles ct on dtq.original_title = ct.title_text
join claims c on ct.claim_id = c.id ;

/* insert tweet-claim relations for searches by URL */
insert into tweet_claim (tweet_id, claim_id, search_by_title, query_validity, match_probability)
select tq.tweet_id,
       c.id,
       false,
       1.0,
       1.0
from tweet_query tq
join dataset_url_query duq on tq.query = duq.tweet_search_url
join claims c on duq.url_id = c.normalized_url_hash ;

