from dataclasses import dataclass

from table_schemas.utils import (
    BaseColumn,
    BaseTable,
    DType,
)

SUPPLEMENTAL_TITLES_DATASET_TABLE_COLUMNS = [
    BaseColumn("id", DType.SERIAL, DType.NOTNULL),
    BaseColumn("url_id", DType.VAR250, DType.NOTNULL),
    BaseColumn("normalized_url", DType.TEXT),
    BaseColumn("archive_url", DType.TEXT),
    BaseColumn("concat_condor_share_title", DType.TEXT),
    BaseColumn("yt_video_headline", DType.TEXT),
    BaseColumn("webpage_title", DType.TEXT),
    BaseColumn("webarchive_search_title", DType.TEXT),
]


@dataclass
class SupplementalTitlesDatasetTable(BaseTable):
    """Dataclass holding information about the titles added to aggregated URLs.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_supplemental_titles"
    columns = SUPPLEMENTAL_TITLES_DATASET_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
