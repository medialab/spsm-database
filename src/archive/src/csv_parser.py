from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import casanova
from casanova import Headers

from constants import WGET_LOG
from path_parser import ArchiveFiles


@dataclass
class RowParser:
    file_length = None
    url_id_pos = None
    archive_url_pos = None
    archive_timestamp_pos = None
    added_columns = ["archive_html_file", "archive_view_uri", "archive_timestamp"]
    default_enricher_addendum = [None, None]

    def __init__(self, headers: Headers, total: int):
        self.select = []
        self.file_length = total
        # Get the URL hash
        self.url_id_pos = headers.get("url_id")
        if not isinstance(self.url_id_pos, int):
            self.url_id_pos = headers["normalized_url_hash"]
            self.select.append("normalized_url_hash")
        else:
            self.select.append("url_id")

        # Get the URL to archive
        self.archive_url_pos = headers["archive_url"]
        self.select.append("archive_url")

        if headers.get("archive_timestamp"):
            self.added_columns.remove("archive_timestamp")
            self.archive_timestamp_pos = headers.get("archive_timestamp")
            self.select.append("archive_timestamp")

        self.default_enricher_addendum = [None for _ in range(len(self.added_columns))]

    def __call__(self, row: List) -> Tuple[str, str]:
        return row[self.url_id_pos], row[self.archive_url_pos]  # type: ignore

    def output(
        self,
        row: List,
        path_parser: ArchiveFiles,
        html_file_path: Path | None,
        archive_time: str | None = None,
    ) -> Tuple[List, List]:
        if html_file_path:
            uri_view = path_parser.make_view_uri(html_file_path)
            addendum = [html_file_path, uri_view]
            if len(self.default_enricher_addendum) == 3:
                addendum.append(archive_time)
                return row, addendum
            else:
                if archive_time:
                    row[self.archive_timestamp_pos] = archive_time  # type:ignore
                return row, addendum
        else:
            return row, self.default_enricher_addendum


class Enricher:
    def __init__(self, infile: str, outfile: str) -> None:
        self.infile = Path(infile)
        self.outfile = Path(outfile)
        total = casanova.count(infile)
        headers = casanova.reader(infile).headers
        if not headers:
            raise ValueError
        self.infile_params = RowParser(headers, total)

    def __enter__(self):
        self.open_infile = open(self.infile, mode="r")
        self.open_outfile = open(self.outfile, mode="w")
        self.open_wget_log = open(WGET_LOG, mode="w")

        return (
            self.open_wget_log,
            casanova.enricher(
                input_file=self.open_infile,
                output_file=self.open_outfile,
                select=self.infile_params.select,
                add=self.infile_params.added_columns,
            ),
            self.infile_params,
        )

    def __exit__(self, exec_type, exec_val, exc_tb):
        if self.open_infile:
            self.open_infile.close()
        if self.open_outfile:
            self.open_outfile.close()
        if self.open_wget_log:
            self.open_wget_log.close()
