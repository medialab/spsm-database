## Archive Web Pages

- Download web pages' content and send the pages to be archived at the Internet Archive; record the log and paths of downloaded files.

from the subdirectory `archive/`

```shell
$ bash archive.sh PATH/TO/MERGED-TABLE.csv
```

Result:

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
