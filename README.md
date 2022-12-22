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
- `bash` (and xsv) script(s) to archive misinformation sources' web pages : 

first positional argument : name of the file in which are the urls of the webpage to save 

second positional argument : name of the folder (to create or not) in which the saved web page will be stored. 
   
   - arhive online all of the web page with `webarchive`
        - save online the web page online 
        - can retrieve the saved webpage afterwards
   
   - archive localy all of the web page with `wget`
        - save localy files from the web page
        - parse log and create a file to save it named '$hash_log'; each file is stored in a folder named 'log_' followed by the first letter or number of the hash of the url 
        - write timestamp to column* in updated merged table
        - create a file containing all the paths to the saved elements of the webpage named '$hash_paths'; each file is stored in a folder named 'hash_' followed by the first letter or number of the hash of the url

  - fetch HTML with `minet fetch`
       - let `minet`update merged table

    \* the column `archive_timestamp` is written and left empty when the merged table is created; it is ready to be used by a new Python script, which should parse the timestamp from the `wget` log and format/write that value into the column
---

[Guildelines for updating the collection of observed appearances of misinformation sources](doc/COLLECTION2.md)

TODO

---
