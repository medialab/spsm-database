# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

When downloading this repository, create a virtual Python environment with the packages `click`, `minet`, `requests`, and `ural`.

---

## Information on data sources in URLs table

### - [How the original sources' data was gathered](doc/data-sources.md)

### - [How the original sources' data was harmonized](doc/normalization.md)

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
