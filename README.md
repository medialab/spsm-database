# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

When downloading this repository, create a virtual Python environment with the packages `click`, `minet`, `requests`, and `ural`.

---
[Guildeines for collecting and formatting data from existing databases](doc/DATASETS.md)


The project's data sources are:
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

---

[Guidelines for updating and archiving the collection of misinformation sources](doc/COLLECTION1.md)

### Merge
- with [merge.py](merge-data/merge.py), aggregate URLs from datasets into one central collection of sources of misinformation.

- with [index.py](merge-data/index.py), map the merged table's CSV columns to value types in an elastic-search index; create that index on the server so it is accessible to the team.

### Archive
- with [archive.py](archive2.0/archive.py), download web pages' content and send the pages to be archived at the [Internet Archive](https://web.archive.org/).
---

[Guildelines for updating the collection of misinformation sources and observed appearances](doc/COLLECTION2.md)

### Misinformation Sources
Using the created CSV files, update the SQL database.
```shell
$ python src/database.py COMMAND FILE
```

Commands currently include: `create-links` (populate table of URLs), `create-condor` (populate table of Condor dataset)

---
