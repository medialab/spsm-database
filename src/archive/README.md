# Archiving processes

This module contains 2 steps for managing the project's archive.

1. Archive URLs using `wget` and WebArchive.org.
2. Ingest information about the archive to the project's SQL database.

## 1. Archive URLs

Run the `wget` command in the script [`src/main.py`](src/main.py) to archive a unified (de-duplicated) set of URLs. If you want to also send the URL to Web Archive, add the `--web-archive` flag to the `wget` command. If you want to skip this step and just use the `wget` process, don't add the flag.

### [WGET archiving script's](src/main.py) required options:

To run the archiving script, call the command `python src/main.py wget`. It requires the following options:

- `-i` : file path to a CSV that contains the URL to archive (column `archive_url`) and an md5 hash of the URL's normalization (column `url_id`)
- `-o` : file path to a CSV that will contain enrich the in-file with information about each URL's archiving
- `-a` : path to the directory in which the root of the archiving will be (from where the WGET command will run)
- `-c` : path to a YAML file that contains connection details for the PostgreSQL database

```console
$ python src/main.py -c <DB CONNECTION CONFIG> -i <URLS FILE> -o <ENRICHED FILE> -a <ARCHIVE ROOT> --web-archive
```

### Test locally

The script will write its results immediately into a PostgreSQL table called "\_archive_in_progress" (see/modify the table name in [src/constants.py](src/constants.py)). Therefore, to test this script locally, set up a database with the table:

1. Start a [PostgreSQL](https://www.postgresql.org/download/) instance.

2. Create a database: `createdb -h localhost -p 5432 -U "username" test-archive`

3. Connect to the test database: `psql -h localhost -p 5432 -U "username" -d test-archive`

4. Create the archiving-in-progress table: `create table "_archive_in_progress" (url_id varchar(250) primary key, archive_url text, archive_timestamp_utc timestamp, archive_html_file text, archive_view_uri text, screen_id varchar(250));`

Next, write the test database's connection details in a YAML configuration file:

```yaml
---
connection:
  db_name: "test-archive"
  db_user: "username"
  db_password: ""
  db_port: "5432"
  db_host: "localhost"
```

Finally, run the script on a CSV file with the following columns:

| **url_id** | **archive_url** |
| ---------- | --------------- |
| 12345      | https://...     |

```console
$ python src/main.py -i INFILE -c CONFIG -o OUTFILE -a ARCHIVE
```

### How's it work?

For example, let's say you provide the path `/store/fakenews/archive-web/archive2.0/` to the option `-a` (`--archive-dir`). When processing a URL with the hash `6dbe42414220727f0552aba43f202501`, the script will create the following folders descending from the archive directory.

`/store/fakenews/archive-web/archive2.0/`

```
├── 6_archive
|   └── 6db
|       ├── assets-global.website-files.com
|       ├── avecvous.fr
|       └── ...
├── 6_log
|   └── 6dbe42414220727f0552aba43f202501_log
└── 6_path
    └── 6dbe42414220727f0552aba43f202501_path
```

The output file contains the 2 required columns, `archive_url` and `url_id` or `normalized_url_hash`, plus the following additional columns:

- `archive_html_file` : Absolute path to the archived index file on the server.
- `archive_view_uri` : Path to view the archived web page in a browser.
- `archive_timestamp` : Time the web page was archived on the server.

### Notes

- If you want to manually skip a URL being archived on the server or being sent to Web Archive, enter control-C one time. This "keyboard interruption" will be caught during the two archiving procedures and let the script move forward.

  `src/main.py`

  ```python
  try:
      subprocess.run(
          # ...
          # WGET or CURL (Web Archive) process
          # ...
      )
  except KeyboardInterrupt:
      pass
  ```

- If for any reason you want to stop and restart archiving your set of URLs, you can run the same command with the same input file and the script will skip over any URLs whose archived files it already finds on the server. Before archiving anything, the script searches for the URL's archive (seen below in the variable `html_file_path`), and if it finds it (if the value is not `None`), it moves on.

  `src/main.py`

  ```python
  if html_file_path:
      wget_log.write(
          f"[{datetime.utcnow()}]\tSkipping\t{url_id}\t'{html_file_path}'\n"
      )
  ```

  `wget.log`

  ```log
  [2024-02-07 13:50:43.488858]	Skipping	856f4bb65d6560e6507b10ae9fcec1fe	'/store/fakenews/archive-web/archive2.0/8_archive/856/atlantico.fr/article/pepite/la-mairie-de-paris-refuse-toujours-de-transmettre-les-notes-de-frais-d-anne-hidalgo-malgre-les-requetes-du-journaliste-stefan-de-vries-conseil-d-etat-avocat-association-journalisme-frais-soutien-aide.html'

  ```

- When in doubt about what URLs were processed, consult the `./wget.log`, which is generated from the current working directory / where you were when you started the script. The log is appended in real-time with a line for every URL, saying whether it was skipped (above) or whether it is being archived. In the latter case, the log is appended as soon as the archiving with `wget` begins and the date reflects the start of the process.

### Integrate archive into urls table

After updating the `_archive_in_progress` table, you might want to integerate that new information into the permanent `urls` table in the SPSM database. (If you're worried about altering this table, export it first.) Run the following SQL:

```sql
update urls
set
    archive_timestamp = aip.archive_timestamp_utc,
    archive_html_file = aip.archive_html_file,
    archive_view_uri = aip.archive_view_uri
from "_archive_in_progress" aip
where urls.id = aip.url_id
```

## 2. Ingest information

### Find HTML files via URL ID

To simply find the URLs whose files have already been saved in the server's archive, run the [`get_html_file_paths/main.py`](get_html_file_paths/main.py) module. This script is useful if you don't have the output of the current archiving procedure.

Options:

- `-a` : Path to the root of the archive.
- `-i` : Path to the CSV file with the targeted URLs; it must contain a column with the URL's md5 hash (`url_id`).
- `-o` : Path to the enriched CSV file that will have the file-path information gathered from the archive.

```console
$ python get_html_file_paths/main.py -i <URLS FILE> -o <ENRICHED FILE> -a <ARCHIVE ROOT>
```

For all the URLs in the input file, it returns an output file with the following additional columns:

- `found_archived_html` : True/False
- `archived_html_path` : Absolute path to the index file on the server.
- `archive_html_base_ref` [outmoded]
