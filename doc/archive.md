## Archive Web Pages

Working from a dataset of aggregated URLs, the script [`archive.py`](../src/archive/archive.py) loops through every URL and performs 2 tasks.

1. It sends the URL to the Internet Archive to be archived.
2. It downloads the page and those of its dependent filepaths.

The URL that is actually archived is not the URL's normalization because the normalization lacks a protocol. Instead, the archiving is done using the URL in the column `archive_url`, which may or may not be slighly different than other URLs aggregated under the same URL normalization.

Archiving produces a local archive with a file based on the archive URL's `url_id` (hash of its normalization). In general, 3 types of directories are created.

1. `log_[0-9|A-Z]` : directory in which to store the log file produced by the `wget` archiving command
2. `path_[0-9|A-Z]` : directory in which to store the text file the script writes containing paths to all the files created during the archiving of a URL
3. `[0-9|A-Z]` : directory in which to store a subdirectory that will store all the directories and files created during the archiving process

Each of these top-level directories contains a single character that represents the first in the archived URL's `url_id`. This limits how many URLs are archived within one directory. Limiting the number of URLs archived in one directory is important because a file system can only handle so many subdirectories inside one directory, and the archiving process generates many files and subdirectories for each processed URL.

An example of this file structure is demonstrated below using the examples of 3 URLs, all of whose `url_id` begins with the character `0`.

```mermaid
flowchart LR

archive("archive/")
script(archive.sh)
log_0("log_0/")
path_0("path_0/")
log1[/000e6870e9a9c1e1d045ebe34a703364_log/]
log2[/000ceb74a81a3d6432ecc89765dadbb9_log/]
log3[/00af1db274f277ca5e19349c2b51f8eb_log/]
path1[/000e6870e9a9c1e1d045ebe34a703364_paths/]
path2[/000ceb74a81a3d6432ecc89765dadbb9_paths/]
path3[/00af1db274f277ca5e19349c2b51f8eb_paths/]
archive0("0/")
archive000[("000/")]
archive00a[("00a/")]
id1{{directories for 000e6870e9a9c1e1d045ebe34a703364}}
id2{{directories for 000ceb74a81a3d6432ecc89765dadbb9}}
id3{{directories for 00af1db274f277ca5e19349c2b51f8eb}}

archive---log_0
archive---script
archive---path_0
archive---archive0

log_0---log1
log_0---log2
log_0---log3
path_0---path1
path_0---path2
path_0---path3

archive0---archive000
archive0---archive00a
archive000---id1
archive000---id2
archive00a---id3


```
