from dataclasses import dataclass
from table_schemas.utils import BaseColumn, BaseTable, DType

SCIENCE_FEEDBACK_DATASET_TABLE_COLUMNS = [
    BaseColumn("claim_appearance_id", DType.VAR20, DType.NOTNULL),
    BaseColumn("claim_url", DType.TEXT),
    BaseColumn("normalized_claim_url", DType.TEXT),
    BaseColumn("normalized_claim_url_hash", DType.VAR250, DType.NOTNULL),
    BaseColumn("claim_reviewed", DType.TEXT),
    BaseColumn("claim_publication_date", DType.DATETIME),
    BaseColumn("claim_publisher", DType.TEXT),
    BaseColumn("first_claim_appearance_review_author", DType.TEXT),
    BaseColumn("first_claim_appearance_review_rating_value", DType.FLOAT),
    BaseColumn("first_claim_appearance_review_rating_standard_form", DType.TEXT),
    BaseColumn("first_claim_appearance_review_url", DType.TEXT),
    BaseColumn("updated_review_date", DType.DATETIME),
    BaseColumn("claim_url_content_id", DType.VAR20, DType.NOTNULL),
    BaseColumn("claim_url_content_review_rating_value", DType.FLOAT),
    BaseColumn("claim_url_content_review_rating_alternate_name", DType.TEXT),
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
        pk_column = getattr(self, "claim_appearance_id")
        self.pk = pk_column.name
