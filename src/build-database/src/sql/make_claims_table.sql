drop table if exists claims cascade ;


create table claims (id SERIAL primary key, normalized_url text, normalized_url_hash varchar(250), condor_table_id integer, defacto_id text, science_feedback_id varchar(20), publication_time timestamp, fact_check_time timestamp, fact_checked_false boolean, fact_checked_true boolean, title_from_concatenated_condor text, title_from_html text, title_from_youtube text, title_from_webarchive text, title_from_condor TEXT) ;

/* Insert claims from Condor dataset */
insert into claims (normalized_url, normalized_url_hash, condor_table_id, publication_time, fact_check_time, fact_checked_false, fact_checked_true)
select dataset.normalized_clean_url,
       dataset.normalized_clean_url_hash,
       dataset.id,
       dataset.first_post_time,
       dataset.tpfc_first_fact_check,
       case
           when dataset.tpfc_rating like '%false%' then true
           else false
       end,
       case
           when dataset.tpfc_rating like '%true%' then true
           else false
       end
from dataset_condor dataset ;


alter table claims add constraint condor_fk
foreign key (condor_table_id) references dataset_condor (id) ;


update claims
set title_from_concatenated_condor = subquery.concatenated_condor_share_titles
from
    (select dst.concatenated_condor_share_titles as concatenated_condor_share_titles,
            dataset.id as condor_id
     from dataset_condor dataset
     join dataset_supplemental_titles dst on dataset.normalized_clean_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;


update claims
set title_from_condor = dataset.share_title
from dataset_condor dataset
where claims.condor_table_id = dataset.id ;


update claims
set title_from_html = subquery.webpage_title
from
    (select dst.webpage_title as webpage_title,
            dataset.id as condor_id
     from dataset_condor dataset
     join dataset_supplemental_titles dst on dataset.normalized_clean_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;


update claims
set title_from_youtube = subquery.yt_video_headline
from
    (select dst.yt_video_headline as yt_video_headline,
            dataset.id as condor_id
     from dataset_condor dataset
     join dataset_supplemental_titles dst on dataset.normalized_clean_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;


update claims
set title_from_webarchive = subquery.webarchive_search_title
from
    (select dst.webarchive_search_title as webarchive_search_title,
            dataset.id as condor_id
     from dataset_condor dataset
     join dataset_supplemental_titles dst on dataset.normalized_clean_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;

/* Insert claims from De Facto dataset */
insert into claims (normalized_url, normalized_url_hash, defacto_id, publication_time, fact_check_time, fact_checked_false, fact_checked_true)
select dataset.normalized_claim_url,
       dataset.normalized_claim_url_hash,
       dataset.id,
       dataset.claim_publication_date,
       dataset.review_publication_date,
       case dataset.claim_rating_value
           when 1 then true
           else false
       end,
       case dataset.claim_rating_value
           when 5 then true
           else false
       end
from dataset_de_facto dataset ;


alter table claims add constraint defacto_fk
foreign key (defacto_id) references dataset_de_facto (id) ;


update claims
set title_from_concatenated_condor = subquery.concatenated_condor_share_titles
from
    (select dst.concatenated_condor_share_titles as concatenated_condor_share_titles,
            dataset.id as defacto_id
     from dataset_de_facto dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.defacto_id = subquery.defacto_id ;


update claims
set title_from_html = subquery.webpage_title
from
    (select dst.webpage_title as webpage_title,
            dataset.id as defacto_id
     from dataset_de_facto dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.defacto_id = subquery.defacto_id ;


update claims
set title_from_youtube = subquery.yt_video_headline
from
    (select dst.yt_video_headline as yt_video_headline,
            dataset.id as defacto_id
     from dataset_de_facto dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.defacto_id = subquery.defacto_id ;


update claims
set title_from_webarchive = subquery.webarchive_search_title
from
    (select dst.webarchive_search_title as webarchive_search_title,
            dataset.id as defacto_id
     from dataset_de_facto dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.defacto_id = subquery.defacto_id ;

/* Insert claims from Science Feedback dataset */
insert into claims (normalized_url, normalized_url_hash, science_feedback_id, publication_time, fact_check_time, fact_checked_false, fact_checked_true)
select dataset.normalized_claim_url,
       dataset.normalized_claim_url_hash,
       dataset.claim_appearance_id,
       dataset.claim_publication_date,
       dataset.updated_review_date,
       case dataset.first_claim_appearance_review_rating_value
           when 1 then true
           else false
       end,
       case dataset.claim_rating_value
           when 5 then true
           else false
       end
from dataset_science_feedback dataset ;


alter table claims add constraint science_fk
foreign key (science_feedback_id) references dataset_science_feedback (claim_appearance_id) ;


update claims
set title_from_concatenated_condor = subquery.concatenated_condor_share_titles
from
    (select dst.concatenated_condor_share_titles as concatenated_condor_share_titles,
            dataset.claim_appearance_id as science_feedback_id
     from dataset_science_feedback dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.science_feedback_id = subquery.science_feedback_id ;


update claims
set title_from_html = subquery.webpage_title
from
    (select dst.webpage_title as webpage_title,
            dataset.claim_appearance_id as science_feedback_id
     from dataset_science_feedback dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.science_feedback_id = subquery.science_feedback_id ;


update claims
set title_from_youtube = subquery.yt_video_headline
from
    (select dst.yt_video_headline as yt_video_headline,
            dataset.claim_appearance_id as science_feedback_id
     from dataset_science_feedback dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.science_feedback_id = subquery.science_feedback_id ;


update claims
set title_from_webarchive = subquery.webarchive_search_title
from
    (select dst.webarchive_search_title as webarchive_search_title,
            dataset.claim_appearance_id as science_feedback_id
     from dataset_science_feedback dataset
     join dataset_supplemental_titles dst on dataset.normalized_claim_url_hash = dst.url_id) as subquery
where claims.science_feedback_id = subquery.science_feedback_id ;

/* Insert claims from Completed URLs dataset */
insert into claims (normalized_url, normalized_url_hash, condor_table_id, publication_time, fact_check_time, fact_checked_false, fact_checked_true)
select dataset.completed_normalized_url,
       dataset.completed_normalized_url_hash,
       dc.id,
       dc.first_post_time,
       dc.tpfc_first_fact_check,
       case
           when dc.tpfc_rating like '%false%' then true
           else false
       end,
       case
           when dc.tpfc_rating like '%true%' then true
           else false
       end
from dataset_completed_urls dataset
join dataset_condor dc on dataset.condor_table_id = dc.id ;


update claims
set title_from_concatenated_condor = subquery.concatenated_condor_share_titles
from
    (select dst.concatenated_condor_share_titles as concatenated_condor_share_titles,
            dc.id as condor_id
     from dataset_completed_urls dataset
     join dataset_condor dc on dc.id = dataset.condor_table_id
     join dataset_supplemental_titles dst on dataset.completed_normalized_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;


update claims
set title_from_html = subquery.webpage_title
from
    (select dst.webpage_title as webpage_title,
            dc.id as condor_id
     from dataset_completed_urls dataset
     join dataset_condor dc on dc.id = dataset.condor_table_id
     join dataset_supplemental_titles dst on dataset.completed_normalized_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;


update claims
set title_from_youtube = subquery.yt_video_headline
from
    (select dst.yt_video_headline as yt_video_headline,
            dc.id as condor_id
     from dataset_completed_urls dataset
     join dataset_condor dc on dc.id = dataset.condor_table_id
     join dataset_supplemental_titles dst on dataset.completed_normalized_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;


update claims
set title_from_webarchive = subquery.webarchive_search_title
from
    (select dst.webarchive_search_title as webarchive_search_title,
            dc.id as condor_id
     from dataset_completed_urls dataset
     join dataset_condor dc on dc.id = dataset.condor_table_id
     join dataset_supplemental_titles dst on dataset.completed_normalized_url_hash = dst.url_id) as subquery
where claims.condor_table_id = subquery.condor_id ;

/* Create URL enrichment table so it includes all URLs in database/claims table */
drop table if exists enrichment_by_url cascade ;


create table enrichment_by_url (id varchar(250) primary key, normalized_url text, archive_url text, title_from_concatenated_condor text, title_from_html text, title_from_webarchive text, title_from_youtube text) ;


insert into enrichment_by_url (id, normalized_url, archive_url, title_from_concatenated_condor, title_from_html, title_from_webarchive, title_from_youtube)
select url_id,
       normalized_url,
       archive_url,
       concatenated_condor_share_titles,
       webpage_title,
       webarchive_search_title,
       yt_video_headline
from dataset_supplemental_titles ;


insert into enrichment_by_url (id)
select normalized_url_hash
from claims on conflict do nothing ;


alter table claims add constraint claim_url_fk
foreign key (normalized_url_hash) references enrichment_by_url (id) ;


alter table dataset_supplemental_titles add constraint dataset_url_fk
foreign key (url_id) references enrichment_by_url (id) ;

