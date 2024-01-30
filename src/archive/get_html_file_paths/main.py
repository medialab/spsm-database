from pathlib import Path

import casanova
import click
import dotenv
from archive_files import ArchiveFiles
from path_management import HTMLFilePath
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

ProgressBar = Progress(
    TextColumn("[progress.description]{task.description}"),
    BarColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
)


class DefaultArchive:
    path = None

    def __init__(self) -> None:
        env_vars = dotenv.dotenv_values()
        archive_path = env_vars.get("ARCHIVE")
        if archive_path:
            self.path = Path(archive_path).resolve().absolute()


DEFAULT_ARCHIVE = DefaultArchive().path


class ArchiveType(click.ParamType):
    name = "Path to the archive directory, in which all the created files are stored."

    def convert(self, value, param, context) -> Path:
        if value and not Path(value).is_dir():
            self.fail(f"\nNot a directory: '{value}'", param, context)
        return Path(value).resolve().absolute()


class InFileType(click.ParamType):
    name = "Path to the CSV file that has the archived URLs and their associated ID."

    def convert(self, value, param, context) -> Path:
        fp = Path(value)
        if not fp.is_file():
            self.fail("Must provide path to a file.", param, context)

        try:
            with casanova.reader(fp) as reader:
                fieldnames = reader.fieldnames
        except Exception:
            self.fail("Failed to open the in-file.", param, context)

        if not fieldnames:
            self.fail("In-file lacks headers.")

        if not "url_id" in fieldnames:
            self.fail("In-file must have the header 'url_id'.", param, context)

        if not "archive_url" in fieldnames:
            self.fail("In-file must have the header 'archive_url'.", param, context)

        return fp.resolve().absolute()


class OutFileType(click.ParamType):
    name = "Path to the CSV file that will be a new version of the in-file, enriched with columns denoting if the URL was successfully archived and where its main HTML page is."

    def convert(self, value, param, context) -> Path:
        fp = Path(value)
        return fp.resolve().absolute()


@click.command()
@click.option("--archive", "-a", type=ArchiveType(), default=DEFAULT_ARCHIVE)
@click.option("--infile", "-i", required=True, type=InFileType())
@click.option("--outfile", "-o", required=True, type=OutFileType())
def main(archive, infile, outfile):
    path_finder = HTMLFilePath(parent=archive)

    total_urls = casanova.count(infile)

    with open(infile, "r") as f, open(outfile, "w") as of, ProgressBar as p:
        enricher = casanova.enricher(
            f,
            of,
            add=["found_archived_html", "archived_html_path", "archive_html_base_ref"],
        )
        t = p.add_task(description="[bold blue]Parsing file paths...", total=total_urls)
        for row, url_id in enricher.cells("url_id", with_rows=True):
            archived = False
            archive_base_ref = ArchiveFiles(url_id=url_id, parent=archive).archive
            html_file = path_finder(url_hash=url_id)
            if html_file:
                archived = True
            enricher.writerow(row, [archived, html_file, archive_base_ref])
            p.advance(t)


if __name__ == "__main__":
    main()
