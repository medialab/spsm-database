from pathlib import Path

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
)

POSTGRES_TABLE_NAME = "_archive_in_progress"

SRC_DIR = Path(__file__).parent
ROOT_DIR = SRC_DIR.parent
SCRIPT_DIR = ROOT_DIR.joinpath("scripts")

WEBARCHIVE_SCRIPT = SCRIPT_DIR.joinpath("webarchive.sh")
WGET_SCRIPT = SCRIPT_DIR.joinpath("wget.sh")
WGET_CLEANUP_SCRIPT = SCRIPT_DIR.joinpath("wget_cleanup.sh")
WGET_LOG = Path.cwd().joinpath("wget.log")

if not WEBARCHIVE_SCRIPT.is_file():
    raise FileNotFoundError(WEBARCHIVE_SCRIPT)
if not WGET_SCRIPT.is_file():
    raise FileNotFoundError(WGET_SCRIPT)


ProgressBar = Progress(
    TextColumn("[bold yellow]{task.description}..."),
    BarColumn(),
    MofNCompleteColumn(),
    TimeElapsedColumn(),
)
