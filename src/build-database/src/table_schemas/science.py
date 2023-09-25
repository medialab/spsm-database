from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

SCIENCE_FEEDBACK_DATASET_TABLE_COLUMNS = [
    BaseColumn("id", DType.VAR20, DType.NOTNULL),
    BaseColumn("normalized_claim_url_hash", DType.VAR250, DType.NOTNULL),
    BaseColumn("claim_url_content_id", DType.VAR20, DType.NOTNULL),
    BaseColumn("claim_reviewed", DType.TEXT),
    BaseColumn("published_date", DType.DATETIME),
    BaseColumn("publisher", DType.TEXT),
    BaseColumn("review_author", DType.TEXT),
    BaseColumn("review_rating_value", DType.FLOAT),
    BaseColumn("review_rating_standard_form", DType.TEXT),
    BaseColumn("claim_url", DType.TEXT),
    BaseColumn("normalized_claim_url", DType.TEXT),
    BaseColumn("claim_url_rating_name", DType.TEXT),
    BaseColumn("claim_url_rating_value", DType.FLOAT),
    BaseColumn("updated_date", DType.DATETIME),
    BaseColumn("review_url", DType.TEXT),
    BaseColumn("review_or_url_rating_value", DType.FLOAT),
]


@dataclass
class ScienceFeedbackDatasetTable(BaseTable):
    """Dataclass holding information about the science feedback data
    source.

    Attributes required by the class's base (BaseTable):
    - name (str) : Name of the table
    - columns (list[BaseColumn]) : Array of BaseColumn objects
    - pk (str) : Primary key / name of the column
    """

    name = "dataset_science_feedback"
    columns = SCIENCE_FEEDBACK_DATASET_TABLE_COLUMNS

    def __init__(self):
        for col in self.columns:
            setattr(self, col.name, col)
        pk_column = getattr(self, "id")
        self.pk = pk_column.name
