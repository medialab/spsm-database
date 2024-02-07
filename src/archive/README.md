# Archiving processes

This module contains 2 steps for managing the project's archive.

1. Archive URLs using `wget` and WebArchive.org.
2. Ingest information about the archive to the project's SQL database.

## 1. Archive URLs

Run the script [`src/main.py`](src/main.py) to archive a unified (de-duplicated) set of URLs. The module requires input and output files. The input file must be a CSV that contains the URL to archive (column `archive_url`) and an md5 hash of the URL's normalization (column header `url_id` or `normalized_url_hash`). The script can run from anywhere if you provide a path to the root of the archive in which you want `wget` to construct its file systems. Otherwise, it will create the archive file system from your current working directory. Lastly, if you want to send the URL to Web Archive, add the `--web-archive` flag to the command. If you want to skip this step and just use the `wget` process, don't add the flag.

```console
$ python src/main.py -i <URLS FILE> -o <ENRICHED FILE> -a <ARCHIVE ROOT> --web-archive
```

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

## 2. Ingest information

### Find HTML files via URL ID

To simply find the URLs whose files have been saved on the server, run the [`get_html_file_paths/main.py`](get_html_file_paths/main.py) module. This script is useful if you don't have the output of the current archiving procedure.

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

### Match the HTML archive to the database's `claims` table
