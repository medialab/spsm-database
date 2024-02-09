import subprocess
import time
from datetime import datetime
from pathlib import Path

import click
from casanova import Enricher

from constants import WEBARCHIVE_SCRIPT, WGET_SCRIPT, ProgressBar
from csv_parser import Enricher
from path_parser import ArchiveFiles


@click.command
@click.option(
    "--infile",
    "-i",
    type=click.Path(exists=True, readable=True),
    required=True,
    help="Claims table",
)
@click.option(
    "--outfile",
    "-o",
    type=click.Path(writable=True),
    required=True,
    help="Path to enriched claims table, with new columns with archive info",
)
@click.option(
    "--archive-dir",
    "-a",
    type=click.Path(dir_okay=True, file_okay=False, exists=True),
    required=False,
    default=Path.cwd(),
    help="Path to the archive directory",
)
@click.option(
    "--web-archive",
    is_flag=True,
    show_default=True,
    default=False,
    help="Send to Web Archive",
)
def main(infile: str, outfile: str, archive_dir: str, web_archive: bool):
    with Enricher(infile, outfile) as e:
        wget_log, enricher, row_parser = e

        with ProgressBar as p:
            wget_task = p.add_task("", total=row_parser.file_length)

            if web_archive:
                webarchive_task = p.add_task(
                    "[bold blue]Sending to Web Archive", total=row_parser.file_length
                )

            for row in enricher:
                # Using the in-file's parsed column headers, select the URL and hash/ID
                url_id, archive_url = row_parser(row)
                p.update(wget_task, description=f"Archiving '{url_id}'")

                # Using the URL hash/ID, parse the file paths created for this URL
                path_parser = ArchiveFiles(url_id=url_id, archive_root=archive_dir)

                # If the URL has already been arcived, skip it and write the file path
                html_file_path = path_parser.html_file
                if html_file_path and html_file_path.stat().st_size > 0:
                    wget_log.write(
                        f"[{datetime.utcnow()}]\tSkipping\t{url_id}\t'{html_file_path}'\n"
                    )
                    row, add = row_parser.output(row, path_parser, html_file_path)

                # Otherwise, archive the URL on the server
                else:
                    archive_time = datetime.utcnow()
                    wget_log.write(
                        f"[{archive_time}]\tArchiving\t{url_id}\t'{archive_url}'\n"
                    )
                    try:
                        # Run the WGET command with the URL
                        subprocess.run(
                            [
                                WGET_SCRIPT,
                                path_parser.archive,
                                archive_url,
                                path_parser.rel_log,
                                path_parser.rel_paths,
                            ]
                        )
                    except KeyboardInterrupt:
                        pass

                    html_file_path = path_parser.html_file
                    row, add = row_parser.output(
                        row=row,
                        path_parser=path_parser,
                        html_file_path=html_file_path,
                        archive_time=archive_time,
                    )

                enricher.writerow(row, add)
                p.advance(wget_task)

                if web_archive:
                    try:
                        print(
                            f"[{datetime.utcnow()}]\tSending URL to Web Archive\t'{archive_url}'"
                        )
                        # Run the CURL command to save the URL to Web Archive
                        subprocess.run([WEBARCHIVE_SCRIPT, archive_url])
                        time.sleep(3)
                    except KeyboardInterrupt:
                        pass

                    p.advance(webarchive_task)  # type: ignore


if __name__ == "__main__":
    main()
