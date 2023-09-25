drop table if exists tweet_claim ;


create table tweet_claim (id serial primary key, tweet_id varchar(20), claim_id integer, search_by_title boolean, query_title_is_same_as_raw_title boolean, match_probability float) ;

/* Insert tweet-claim reltions for searches by title */
insert into tweet_claim (tweet_id, claim_id, search_by_title, query_title_is_same_as_raw_title, match_probability)
select tq.tweet_id,
       c.id,
       TRUE,
       dtq.same_as_original,
       case
           when dtq.same_as_original then 0.25
           when ct.title_origin = 'concatenated condor' then 0.0
           else 0.5
       end
from tweet_query tq
join dataset_title_query dtq on tq.query = dtq.tweet_search_title
join claim_titles ct on dtq.original_title = ct.title_text
join claims c on ct.claim_id = c.id ;


alter table tweet_claim add constraint claim_fk
foreign key (claim_id) references claims (id) ;


alter table tweet_claim add constraint tweet_fk
foreign key (tweet_id) references tweet (id) ;