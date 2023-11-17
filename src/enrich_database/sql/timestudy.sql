select foo.fact_check_time,
       foo.tweet_time,
       foo.fact_checked_true,
       foo.fact_checked_false,
       dc.tpfc_rating,
       foo.claim_id,
       foo.claim_url_id,
       foo.query,
       foo.search_by_title,
       foo.tweet_id,
       foo.retweeted_id,
       foo.quoted_id,
       foo.user_id,
       foo.unique_condor_id,
       foo.unique_defacto_id,
       foo.unique_science_feedback_id,
       extract (DAY
                from foo.diff) * 86400 + extract (HOUR
                                                  from foo.diff) * 3600 + extract (MINUTE
                                                                                   from foo.diff) * 60 + extract (SECOND
                                                                                                                  from foo.diff) as diff_seconds
from
  (select t.timestamp_utc - c.fact_check_time as diff,
          c.fact_check_time,
          c.fact_checked_true,
          c.fact_checked_false,
          c.id as claim_id,
          c.normalized_url_hash as claim_url_id,
          tq.query,
          tc.search_by_title,
          tq.tweet_id,
          t.timestamp_utc as tweet_time,
          t.retweeted_id,
          t.quoted_id,
          t.user_id,
          c.condor_table_id as unique_condor_id,
          c.defacto_id as unique_defacto_id,
          c.science_feedback_id as unique_science_feedback_id
   from claims c
   join tweet_claim tc on tc.claim_id = c.id
   join tweet_query tq on tc.tweet_id = tq.tweet_id
   join tweet t on tc.tweet_id = t.id) foo
left join dataset_condor dc on foo.unique_condor_id = dc.id