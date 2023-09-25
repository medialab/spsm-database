drop table if exists claim_titles ;


create table claim_titles(claim_id integer, title_text text, title_origin text) ;


alter table claim_titles add constraint pk primary key (claim_id,
                                                        title_text) ;


insert into claim_titles (claim_id, title_text, title_origin)
select foo.claim_id,
       foo.title,
       foo.title_origin
from
    (select id as claim_id,
            title_from_html as title,
            'html' as title_origin
     from claims
     where title_from_html is not null
     union all select id as claim_id,
                      title_from_youtube as title,
                      'youtube' as title_origin
     from claims
     where title_from_youtube is not null
     union all select id as claim_id,
                      title_from_webarchive as title,
                      'web archive' as title_origin
     from claims
     where title_from_webarchive is not null
     union all select id as claim_id,
                      title_from_concatenated_condor as title,
                      'concatenated condor' as title_origin
     from claims
     where title_from_concatenated_condor is not null
     union all select id as claim_id,
                      title_from_condor as title,
                      'condor' as title_origin
     from claims
     where title_from_condor is not null ) as foo
group by foo.claim_id,
         foo.title,
         foo.title_origin on conflict DO NOTHING;


alter table claim_titles add constraint claim_fk
foreign key (claim_id) references claims (id) ;

