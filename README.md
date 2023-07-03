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

Create initial tables from CSV files. To guarantee that the database is always constructed in the same way, declare in the config file the fixed CSV files used for the import. The following, finalized data files have been used and are stored on a private git repository: [Condor](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/condor_full.csv), [Completed URLs](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/unique_completed_urls_from_condor_set_of_duplicate_urls.csv), [URLs' enriched titles](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/url_title_enrichment.csv), [Science Feedback](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/science_feedback_full.json), [De Facto](https://github.com/medialab/spsm-data/blob/main/database-files/for_import/defacto_full.json).

```yaml
---
data sources:
  condor: "/PATH/"
  completed urls: "/PATH/"
  science feedback: "/PATH/"
  de facto: "/PATH/"
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

#### Update the 3 former sources table with the enriched titles from the imported dataset.

```shell
$ python src/build-database/main.py config.yml sources
```

---

### Claim Table

TO DO

### Step 2. Import Tweet data

Parse files of tweet results and populate SQL tables for the `tweet`, the `twitter_user`, and the relationship between a TWeet and the search query that returned it, `tweet_query`.

```shell
$ python src/build-database/main.py config tweets /PATH/TO/RESULTS/FILE
```

![ER diagram](doc/spsm%20-%20public.png)
