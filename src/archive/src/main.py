import subprocess
import time
from datetime import datetime
from pathlib import Path

import casanova
import click
import yaml
from casanova import Enricher
from rich.console import Console, Group
from rich.live import Live
from rich.panel import Panel

from constants import WEBARCHIVE_SCRIPT, WGET_SCRIPT, ProgressBar
from csv_parser import Enricher
from database import PostgresWrapper
from path_parser import ArchiveFiles


@click.group()
def cli():
    pass


@cli.command("webarchive")
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
def webarchive(infile, outfile):
    total = casanova.count(infile)
    console = Console()
    console.clear()
    status = console.status("Not started")
    p = ProgressBar
    with Live(Panel(Group(status, p))), open(infile, "r") as f, open(
        outfile, "w"
    ) as of:
        enricher = casanova.enricher(f, of, add=["web_archive_time", "canceled"])
        t = p.add_task("CURL subprocess", total=total)
        for row, archive_url in enricher.cells("archive_url", with_rows=True):
            status.update(f"[green]Sending to Web Archive\n{archive_url}")
            skipped = False
            archive_time = datetime.utcnow()
            try:
                subprocess.run([WEBARCHIVE_SCRIPT, archive_url])
            except KeyboardInterrupt:
                skipped = True
                status.update(
                    "[red]Stopped wget on this URL.\nQuickly press control-C again to stop the whole script."
                )
                try:
                    time.sleep(2)
                except KeyboardInterrupt:
                    status.update("[red]Stopped whole script.")
                    exit()

            enricher.writerow(row, [archive_time, skipped])
            p.advance(t)


@cli.command("wget")
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
    "--read-time",
    is_flag=True,
    show_default=True,
    default=False,
    help="Read time of found HTML file",
)
def wget(infile: str, outfile: str, archive_dir: str, read_time: bool):
    console = Console()

    with open("config.yml") as f:
        config = yaml.safe_load(f)
    db_wrapper = PostgresWrapper(config)

    with Enricher(infile, outfile) as e:
        wget_log, enricher, row_parser = e

        status = console.status("Not started")
        p = ProgressBar
        with Live(Panel(Group(status, p))):

            wget_task = p.add_task("Wget", total=row_parser.file_length)

            for row in enricher:
                # Using the in-file's parsed column headers, select the URL and hash/ID
                url_id, archive_url = row_parser(row)
                # console.clear()
                status.update(f"[green]Processing '{url_id}'\n{archive_url}")

                # Using the URL hash/ID, parse the file paths created for this URL
                path_parser = ArchiveFiles(url_id=url_id, archive_root=archive_dir)

                # If the URL has already been arcived, skip it and write the file path
                html_file_path = path_parser.html_file
                if html_file_path and html_file_path.stat().st_size > 0:
                    if read_time:
                        archive_time = datetime.fromtimestamp(
                            html_file_path.stat().st_ctime
                        )
                    else:
                        archive_time = None
                    wget_log.write(
                        f"[{datetime.utcnow()}]\tSkipping\t{url_id}\t'{html_file_path}'\n"
                    )
                    uri_view = path_parser.make_view_uri(html_file_path)

                    # Write results to the CSV file
                    row, add = row_parser.output(
                        row=row,
                        uri_view=uri_view,
                        html_file_path=html_file_path,
                        archive_time=archive_time,
                    )

                    # Write results to the Postgres database
                    db_wrapper.insert(
                        url_id=url_id,
                        archive_url=archive_url,
                        archive_timestamp=archive_time,
                        archive_html_file=html_file_path,
                        archive_view_url=uri_view,
                    )

                # Otherwise, archive the URL on the server
                else:
                    archive_time = datetime.utcnow()
                    wget_log.write(
                        f"[{archive_time}]\tArchiving\t{url_id}\t'{archive_url}'\n"
                    )
                    # Launch the WGET command
                    try:
                        process = subprocess.Popen(
                            [
                                WGET_SCRIPT,
                                path_parser.archive,
                                archive_url,
                                path_parser.rel_log,
                                path_parser.rel_paths,
                            ],
                            shell=False,
                        )

                        # Run the command within the time-out interval
                        try:
                            _, errs = process.communicate(timeout=120)
                            if errs:
                                raise OSError(errs)
                        except subprocess.TimeoutExpired:
                            # os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                            process.terminate()

                    # Stop the command with a keyboard interrupt
                    except KeyboardInterrupt as e:
                        status.update(
                            "[red]Stopped wget on this URL.\nQuickly press control-C again to stop the whole script."
                        )
                        try:
                            time.sleep(2)
                        except KeyboardInterrupt as e:
                            status.update("[red]Stopped whole script.")
                            exit()

                    # If the command exited correctly, process the results
                    html_file_path = path_parser.html_file
                    uri_view = path_parser.make_view_uri(html_file_path)

                    # Write the results to the CSV file
                    row, add = row_parser.output(
                        row=row,
                        uri_view=uri_view,
                        html_file_path=html_file_path,
                        archive_time=archive_time,
                    )
                    # Write the results to the Postgres database
                    db_wrapper.insert(
                        url_id=url_id,
                        archive_url=archive_url,
                        archive_timestamp=archive_time,
                        archive_html_file=html_file_path,
                        archive_view_url=uri_view,
                    )

                enricher.writerow(row, add)
                p.advance(wget_task)


if __name__ == "__main__":
    cli()
