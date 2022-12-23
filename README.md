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
- with [archive.sh](archive.sh), `wget` download web pages' content and send the pages to be archived at the [Internet Archive](https://web.archive.org/); save the `wget` log and write paths in log to file.

from the subdirectory `archive/`
```shell
$ bash archive.sh PATH/TO/DATAFILE
```

- TODO: in Python
    1. list all log subdirectories in archive directory (see Python's native [os library](https://docs.python.org/fr/3/library/os.html))
        - iterate through all log subdirectories and all `wget` logs inside each subdirectory
    2. with a `wget` log open,
        - parse URL ID from log file name
        - on first line, parse log date-time (ex. `--2022-12-23 09:46:32--`)
        - on last line, parse success
            - fail: `Liens convertis dans 0 fichiers en 0 secondes.`
            - success: `Liens convertis dans 7 fichiers en 0,004 secondes.`
        - if `wget` download was successful, index date-time to URL ID
        ```python
        {
            "000ceb74a81a3d6432ecc89765dadbb9": "2022-12-23 06:37:55", # successful
            "000e6870e9a9c1e1d045ebe34a703364": None, # unsuccessful
        }
        ```
    4. with merged table open,
        - iterate through merged table while adding a value to `archive_timestamp` column

---

[Guildelines for updating the collection of observed appearances of misinformation sources](doc/COLLECTION2.md)

TODO

---
