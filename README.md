# SPSM Project Database Manager

Tools to create, update, and enrich the SPSM project's data.

---

## Information on data sources in URLs table

### - [How the original sources' data was gathered](doc/data-sources.md)

### - [How the original sources' data was aggregated by URL](doc/normalization.md)

### - Data source statistics:

- Condor
  - start: `2011-01-01 08:10:00`
  - end: `2022-07-05 21:20:00`
  - count: `98,794`
- Science Feedback
  - start: `2008-04-02T23:31:39Z` (not normalized in merged table column `date`)
  - end: `2022-12-16 03:38:15`
  - count: `1,5037`
- De Facto
  - start: `0202-07-06 23:09:21`
  - end: `2022-12-17 00:00:00`
  - count: `290`

### - [How the URLs were archived](doc/archive.md)

---

## Database Entity Relationships

### Tweet Table to Tweet-Query Relational Table

The `tweet` table contains every tweet collected during the course of data collection for the project. The primary key is the column `id`, which represents the Tweet's ID according to Twitter. Tweets collected by search queries are related together via the `tweet_query` relational table. The latter table contains every pairing of tweet and query. The primary key is the composite of the `tweet_id` and `query`, which ensures that the table only contains a unique set of relations between Tweets and search queries.

In the relational `tweet_query` table, the ID of a Tweet (`tweet_id`) can occur many times if a Tweet satisifed more than one query. Likewise, the `query` can occur many times if more than one Tweet matched on the search query.

![tweet/tweet-query relation](doc/ER-Diagram_2.png)

### Tweet Table to User Table

The `tweet` table also relates to the table `user`. The latter's primary key is the column `id`, which relates to the Twitter user's ID according to Twitter.

Note: At the moment (late June 2023), only the Tweet's author (`user_id`) is related to the Twitter users in the `user` table. However, the `user` table is conceived so that it represents a unique set of Twitter users pertinent to the database. Consequently, other fields in the `tweet` table, such as `retweeted_user_id`, also have a relation to the Twitter users in the `user` table. Right now, the data in `user` table is derived from the author of a Tweet in the `tweet` table because the author allows for the population of many of the data fields in the `user` table. However, the `user` table should also contain nearly empty rows corresponding to a Twitter user for whom only the ID is known because it corresponds to a field such as `quoted_user_id`. This modification to the `user` table is in progress.

![tweet/user relation](doc/ER-Diagram_1.png)
