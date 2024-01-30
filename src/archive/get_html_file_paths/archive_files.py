from pathlib import Path


class ArchiveFiles:
    def __init__(self, url_id: str, parent: Path) -> None:
        self.parent = parent
        self.url_id = url_id
        self.prefix = url_id[:1]
        self.archive_parent_dir = url_id[:3]

    @property
    def log(self):
        log_parent = self.prefix + "_log"
        log_file = self.url_id + "_log"
        return self.parent.joinpath(log_parent).joinpath(log_file)

    @property
    def paths(self):
        paths_parent = self.prefix + "_path"
        paths_file = self.url_id + "_paths"
        return self.parent.joinpath(paths_parent).joinpath(paths_file)

    @property
    def archive(self):
        archive_parent = self.prefix + "_archive"
        archive_dir = self.parent.joinpath(archive_parent).joinpath(
            self.archive_parent_dir
        )
        return archive_dir

    def join_to_archive(self, url_path: str | Path) -> Path:
        return self.archive.joinpath(url_path)
