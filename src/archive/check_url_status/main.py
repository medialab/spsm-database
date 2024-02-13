import csv
from argparse import ArgumentParser
from concurrent.futures import ThreadPoolExecutor, as_completed

import casanova
from minet.constants import DEFAULT_URLLIB3_TIMEOUT
from minet.web import request
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)


def main():
    parser = ArgumentParser()
    parser.add_argument("-i", "--infile")
    parser.add_argument("-o", "--outfile")
    args = parser.parse_args()
    INFILE, OUTFILE = args.infile, args.outfile

    total = casanova.count(INFILE)
    with open(INFILE) as f, ThreadPoolExecutor() as pool, open(
        OUTFILE, "w"
    ) as of, Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
    ) as progress:
        reader = casanova.reader(f)
        if not reader.headers:
            raise KeyError
        url_id_pos = reader.headers["url_id"]
        writer = csv.writer(of)
        writer.writerow(["url_id", "archive_url", "status", "exception"])
        task = progress.add_task("Requesting", total=total)
        future_to_url = {
            pool.submit(minet_request, url): (url, row[url_id_pos])
            for row, url in reader.cells("archive_url", with_rows=True)
        }
        for future in as_completed(future_to_url):
            url, url_id = future_to_url[future]
            progress.advance(task)
            try:
                data = future.result()
            except Exception as exc:
                writer.writerow([url_id, url, data.status, exc])
            else:
                writer.writerow([url_id, url, data.status, None])


def minet_request(url):
    return request(url, timeout=DEFAULT_URLLIB3_TIMEOUT)


if __name__ == "__main__":
    main()
