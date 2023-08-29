import csv
import gzip
import sys
from contextlib import contextmanager

import casanova
import click
import spacy
import spacy_fastlang
from tqdm import tqdm

csv.field_size_limit(sys.maxsize)


class LangDetect:
    def __init__(self) -> None:
        self.nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
        self.nlp.add_pipe("language_detector")

    def __call__(self, text: str):
        self.nlp.max_length = len(text) + 100
        lang = None
        if text:
            doc = self.nlp(text)
            lang = doc._.language
        return lang


LANG_COL = "detected_language"


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
@click.option("--infile")
@click.option("--outfile")
def main(infile, outfile):
    # Set up NLP
    nlp = LangDetect()

    total_rows = casanova.reader.count(infile)

    with open_large_file(infile) as f, open(outfile, "w") as of:
        enricher = casanova.enricher(
            f,
            of,
            select=["url_id", "webpage_lang", "webpage_text"],
            add=[LANG_COL],
        )
        for row, webpage_text in tqdm(
            enricher.cells(column="webpage_text", with_rows=True), total=total_rows
        ):
            lang = nlp(webpage_text)
            enricher.writerow(row, [lang])


if __name__ == "__main__":
    main()
