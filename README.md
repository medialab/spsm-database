# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

When downloading this repository, create a virtual Python environment with the packages `click`, `minet`, `requests`, and `ural`.

---
[Guildeines for collecting and formatting data from existing databases](doc/DATASETS.md)

The project's data sources are:
- Condor
    - one-time import (24 October 2022)
- Science Feedback
    - requests must be targeted to a date frame
- De Facto
    - updated regularly
    - requests return entire database

*Science Feedback date frame*

>maybe :  01/01/2020 - 31/12/2022


*Comparable date frame for De Facto*

>maybe :  start (22/12/2020) - 31/12/2022

---

[Guidelines for updating and archiving the collection of misinformation sources](doc/COLLECTION1.md)

### Update
- with [merge.py](merge.py), aggregate URLs from datasets into one central collection of sources of misinformation 

### Archive
- `bash` script(s) to archive misinformation sources' web pages
    - archive all of the web page with `wget`
        - save files
        - parse log
        - write timestamp to column* in updated merged table
    - fetch HTML with `minet fetch`
        - let `minet` update merged table

    \* the column `archive_timestamp` is written and left empty when the merged table is created; it is ready to be used by a new Python script, which should parse the timestamp from the `wget` log and format/write that value into the column
---

[Guildelines for updating the collection of observed appearances of misinformation sources](doc/COLLECTION2.md)

TODO

---