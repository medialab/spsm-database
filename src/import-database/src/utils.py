import csv
import gzip
from pathlib import Path
from typing import Generator

from rich.progress import (
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)


class ProgressBar:
    def __init__(self):
        pass

    def __enter__(self):
        self.progress = Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            MofNCompleteColumn(),
            TimeElapsedColumn(),
        )
        self.progress.start()
        return self.progress

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.stop()


def yield_csv_dict_row(file) -> Generator[dict, None, None]:
    if Path(file).is_file():
        try:
            with open(file, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    yield row
        except UnicodeDecodeError:
            with gzip.open(file, "rt") as f:
                reader = csv.DictReader(f)  # type: ignore
                for row in reader:
                    yield row
