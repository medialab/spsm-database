import re
from pathlib import Path


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


class ArchiveFiles:
    def __init__(self, url_id: str, archive_root: Path | str) -> None:
        self.archive_root = Path(archive_root)
        self.url_id = url_id
        self.prefix = url_id[:1]
        self.archive_parent_dir = url_id[:3]

    @property
    def archive(self):
        archive_parent = self.prefix + "_archive"
        archive_dir = self.archive_root.joinpath(archive_parent).joinpath(
            self.archive_parent_dir
        )
        archive_dir.mkdir(exist_ok=True, parents=True)
        return archive_dir.resolve()

    @property
    def html_file(self):
        path_file = self.paths
        if path_file.is_file():
            parser = PathFileParser()
            with open(path_file, "r", encoding="utf-8") as f:
                first_line = f.readline()
                first_path = parser(first_line)
                if first_path:
                    full_file = self.join_to_archive(first_path)
                    if full_file.is_file():
                        return full_file

    @property
    def log(self):
        log_parent = self.archive_root.joinpath(self.prefix + "_log")
        log_parent.mkdir(exist_ok=True)
        return log_parent.joinpath(self.url_id + "_log")

    @property
    def rel_log(self):
        return self.log.resolve().relative_to(self.archive_root.resolve())

    @property
    def paths(self):
        paths_parent = self.archive_root.joinpath(self.prefix + "_path")
        paths_parent.mkdir(exist_ok=True)
        return paths_parent.joinpath(self.url_id + "_paths")

    @property
    def rel_paths(self):
        return self.paths.resolve().relative_to(self.archive_root.resolve())

    def join_to_archive(self, url_path: str | Path) -> Path:
        return self.archive.joinpath(url_path)

    def make_view_uri(self, html_file_path: Path | None) -> str | None:
        if html_file_path and html_file_path.stat().st_size > 0:
            rel_path = html_file_path.relative_to(self.archive_root.resolve())
            return "http://spsm.reims.sciences-po.fr/webarchives/" + str(rel_path)
