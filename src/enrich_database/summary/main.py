import csv
import gzip
import logging
import sys
from collections import Counter
from contextlib import contextmanager

import casanova
import click
from nlp import NLP
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
)

logging.basicConfig(filename="nlp.log", level=logging.INFO)
csv.field_size_limit(sys.maxsize)

SUPPORTED_LANGUAGES = ["en", "fr"]


@contextmanager
def open_large_file(file: str):
    is_gzipped = True
    try:
        with gzip.open(file, "r") as f:
            f.read()
    except gzip.BadGzipFile:
        is_gzipped = False

    if is_gzipped:
        yield gzip.open(file, "rt")
    else:
        yield open(file, "r")


@click.command()
@click.option("--infile", required=True)
@click.option("--outfile", required=True)
@click.option("--lang", "-l", multiple=True)
def main(infile, outfile, lang):
    # Determine if the target languages are supported with models
    if not all(l in SUPPORTED_LANGUAGES for l in lang):
        raise Exception(
            f'Language not supported. Supported languages include: {", ".join(SUPPORTED_LANGUAGES)}'
        )

    # By initiating the class, download the models
    nlp = NLP(lang)

    # Calculate how much data needs processed
    print("\n\nCounting in-file...")
    lang_counter = Counter()
    file_length = casanova.reader.count(infile)
    with open_large_file(infile) as f:
        reader = casanova.reader(f)
        for dl in reader.cells("detected_language"):
            lang_counter.update([dl])

    # Open files and set up the progress bars
    with open_large_file(infile) as f, open(outfile, "w") as of, Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        MofNCompleteColumn(),
    ) as progress:
        # Add tasks to progress bars
        full_task = progress.add_task("[bold green]Full CSV", total=file_length)
        english_task = progress.add_task(
            "[red]    English summaries", total=lang_counter.get("en")
        )
        french_task = progress.add_task(
            "[blue]    French summaries", total=lang_counter.get("fr")
        )
        enricher = casanova.enricher(
            f, of, select=["url_id", "detected_language"], add=["summary"]
        )

        # Get column indices in the CSV
        lang_pos = enricher.headers.detected_language
        id_pos = enricher.headers.url_id

        # Iterate through the CSV
        for row, text in enricher.cells("webpage_text", with_rows=True):
            dl = row[lang_pos]
            url_id = row[id_pos]

            # Perform inference
            result = nlp(text=text, lang=dl)

            # If the inference succeeded, write it to the out-file
            if isinstance(result, Exception):
                logging.warning("ID: {} | Error: {}".format(url_id, result))
                continue
            elif result:
                enricher.writerow(row, [result])

            # Update the progress bars
            if dl == "en":
                progress.update(task_id=english_task, advance=1)
            elif dl == "fr":
                progress.update(task_id=french_task, advance=1)
            progress.update(task_id=full_task, advance=1)


if __name__ == "__main__":
    main()
