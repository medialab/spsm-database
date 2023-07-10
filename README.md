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

## Database

The database is being created with scripts in [src/build-database](src/build-database/), which take advantage of Python dataclasses to store static information about the tables' original schemas, as they were conceived at the creation of the database. To observe the database's creation locally, install PostgreSQL and create a database ("spsm"). Using your computer's user name (and password if necessary), run the database creation script. You will need a configuration file ([see example](example.config.json)) that details your connection to the PostgreSQL database and lists files of Twitter data you want to import.

### Step 1. Import data from CSV files

Create initial tables from CSV files. To guarantee that the database is always constructed in the same way, declare in the config file the fixed CSV files used for the import. The following, finalized data files have been used and are stored on a private git repository: [Condor](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/condor_full.csv), [Completed URLs](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/unique_completed_urls_from_condor_set_of_duplicate_urls.csv), [URLs' enriched titles (e.g. scraped HTML title, YouTube title, Web Archive title)](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/url_title_enrichment.csv), [Science Feedback](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/science_feedback_full.json), [De Facto](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/defacto_full.json), [Queried titles (original title, cleaned version, whether it was queried)](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/practice-queried-titles.csv).

```yaml
---
data sources:
  condor: "/PATH/"
  completed urls: "/PATH/"
  science feedback: "/PATH/"
  de facto: "/PATH/"
  enriched titles: "/PATH/"
  titles: "/PATH/"
```

#### Import finalized Condor dataset.

```shell
$ python src/build-database/import_sources.py config.yml condor
```

#### Import finalized De Facto dataset.

```shell
$ python src/build-database/import_sources.py config.yml de-facto
```

#### Import finalized Science Feedback dataset.

```shell
$ python src/build-database/import_sources.py config.yml science
```

#### Import table of URLs with enriched titles.

Enriched titles are (1) scraped from the HTML, (2) requested from YouTube, and/or (3) from WebArchive.

```shell
$ python src/build-database/import_sources.py config.yml enriched-titles
```

The [finalized CSV file](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/url_title_enrichment.csv) has the following data fields:

| url_id                      | sources                                                     | normalized_url      | archive_url                                                 | condor_share_title                                 | yt_video_headline                                         | webpage_title                          | webarchive_search_title                                               |
| --------------------------- | ----------------------------------------------------------- | ------------------- | ----------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------- | -------------------------------------- | --------------------------------------------------------------------- |
| Hash of the normalized URL. | Concatenation of sources which contain this normalized URL. | The normalized URL. | An un-normalized version of the URL for archiving purposes. | The title given to this URL in the Condor dataset. | If the URL is of a YouTube video, the title of the video. | The title scraped from the URL's HTML. | The title found on an archived version of the website on Web Archive. |

### Import table of queried titles and their original, pre-cleaned versions.

```shell
$ python src/build-database/import_sources.py config.yml queried-titles
```

TODO: Create this finalized CSV file.

CSV file must have the following columns:

| title_text                                                                                      | tweet_search_title                        | queried                                                      |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------ |
| Text (with leading and trailing white spaces removed) of the original title, prior to cleaning. | Text of the cleaned version of the title. | True or False denoting whether or not the title was queried. |

---

### Step 2. Use imported data to enrich and build tables

```shell
$ python src/build-database/main.py config.yml sources
```

![ER diagram](doc/spsm%20-%20public.png)

TODO: Add SQL to build `url` table out of tables `de_facto`, `science_feedback`, `condor`, and `completed_urls_dataset`.

Steps:

1. Create URL table with an auto-incremengint primary key, allowing for duplicates of the same URL if multiple sources have it and/or if the same source has it more than once.
2. Insert data from 4 dependent tables into the relational `url` table.
3. Alter the table with the tweet-search version of the URL (e.g. `google.com` -> `url:"google.com"`)
4. Alter the table again with the few hundred modified tweet-search versions, resulting from a mistake during the collection process where the parameter was not implemented.

Example of current (10/07/2023) process in terminal:

```
=========================================
Building Completed URL table.

If they have a corresponding Condor URL RID in the Condor table,
update the completed URLs' Condor table ID foreign key by
matching on the original URL hash and the Condor URL RID.

    UPDATE completed_urls_dataset
    SET condor_table_id = s.id
    FROM (
        SELECT  completed_urls_dataset.condor_url_rid,
                completed_urls_dataset.hash_of_original_normalized_url,
                condor.id
        FROM completed_urls_dataset
        INNER JOIN condor
        ON completed_urls_dataset.hash_of_original_normalized_url = condor.normalized_clean_url_hash
        AND completed_urls_dataset.condor_url_rid = condor.condor_url_rid
        ) s
    WHERE s.condor_url_rid IS NOT NULL
    AND completed_urls_dataset.hash_of_original_normalized_url = s.hash_of_original_normalized_url
    AND completed_urls_dataset.condor_url_rid = s.condor_url_rid


If they don't have a corresponding Condor URL RID in the Condor table,
update the completed URLs' Condor table ID foreign key by matching
on the original URL hash and the lack of a Condor URL RID.

    UPDATE completed_urls_dataset
    SET condor_table_id = s.id
    FROM (
        SELECT  completed_urls_dataset.condor_url_rid,
                completed_urls_dataset.hash_of_original_normalized_url,
                condor.id
        FROM completed_urls_dataset
        INNER JOIN condor
        ON completed_urls_dataset.hash_of_original_normalized_url = condor.normalized_clean_url_hash
        ) s
    WHERE s.condor_url_rid IS NULL
    AND completed_urls_dataset.hash_of_original_normalized_url = s.hash_of_original_normalized_url


=========================================
Adding enriched titles to claims in data sources.

Altering De Facto table to have enriched title columns

Altering Science Feedback table to have enriched title columns

Altering Condor table to have enriched title columns

=========================================
Relating claims to titles.

Created table 'claim_title' with the following columns:
id(INTEGER), condor_id(INTEGER), title_text(TEXT), title_type(TEXT), de_facto_id(TEXT), science_feedback_id(CHARACTER VARYING)

Adding Condor share title to relational table 'claim_title'.

Adding scraped HTML titles to relational table 'claim_title'.

Adding YouTube video titles to relational table 'claim_title'.

Adding Web Archive video titles to relational table 'claim_title'.
```

Example of result in `condor` table, in which the entity was updated with a title from YouTube when the original data was lacking a `share_title`:

| id   | condor_url_rid  | url_id                           | normalized_url                  | share_title | ... | title_from_youtube                                      |
| ---- | --------------- | -------------------------------- | ------------------------------- | ----------- | --- | ------------------------------------------------------- |
| 8793 | i130zeund5dnbv1 | 7f719769ddf6b68b0327f0838d53348b | youtube.com/watch?v=ua1RPdQchsc |             | ... | Burger King Admits To Using Horse Meat In Their Burgers |

---

### Step 3. Import Tweet data

Parse files of tweet results and populate SQL tables for the `tweet`, the `twitter_user`, and the relationship between a TWeet and the search query that returned it, `tweet_query`.

```shell
$ python src/build-database/main.py config tweets /PATH/TO/RESULTS/FILE
```

## Querying the relational database

Example research question: _What tweets circulated the title of a claim that Condor fact-checkers had determined was "missing context"?_

The following selection stays the same whenever selecting tweets from the database based on claim's conditions:

```sql
select tweet.*
from tweet
inner join tweet_query on tweet_query.tweet_id = tweet.id
inner join title on title.tweet_search_title = tweet_query.query
inner join claim_title on claim_title.title_text = title.title_text
inner join condor on condor.id = claim_title.condor_id'
```

And the selection is simply modified with a condition at the end:

```sql
where condor.tpfc_rating like '%missing context%'
```

Data can also be selected based on the ID of a claim in the database, which itself can be selected in some other way--perhaps in an operation (in R) outside the database.

For example, say you have determined you need to look at users who circulated a claim from the `science_feedback` table with the ID `12345`.

You would use the following basic selection:

```sql
select twitter_user.*
from tweet
inner join tweet_query on tweet_query.tweet_id = tweet.id
inner join title on title.tweet_search_title = tweet_query.query
inner join claim_title on claim_title.title_text = title.title_text
inner join science_feedback on science_feedback.id = claim_title.science_feedback_id
inner join twitter_user on twitter_user.id = tweet.user_id
```

And you would append it with your condition:

```sql
where science_feedback.id = '12345'
```
