import re
from pathlib import Path

from archive_files import ArchiveFiles


class HTMLFilePath:
    def __init__(self, parent: Path | str) -> None:
        self.parent = Path(parent)

    def __call__(
        self,
        url_hash: str,
    ) -> Path | None:
        # From the URL ID and the archive dir (parent), parse the URL's archive files
        url_paths = ArchiveFiles(url_id=url_hash, parent=self.parent)
        parser = PathFileParser()

        # Open the archive URL's paths log to find the main index page
        if url_paths.paths.is_file():
            with open(url_paths.paths, "r", encoding="utf-8") as f:
                first_line = f.readline()
                first_path = parser(first_line)

                if first_path:
                    full_file = url_paths.join_to_archive(first_path)

                    if full_file.is_file():
                        return full_file


class PathFileParser:
    def __init__(self) -> None:
        self.lang = None

    def __call__(self, line):
        if not self.lang:
            if line.split(" ")[0].lower() == "Sauvegarde".lower():
                return self.french_regex(line)
            else:
                return self.english_regex(line)

    def english_regex(self, line: str):
        match = re.match(r"Saving to: ‘(.*)’", line)
        if match:
            return match.group(1)

    def french_regex(self, line: str):
        match = re.match(r"Sauvegarde en : « (.*) »", line)
        if match:
            return match.group(1)
