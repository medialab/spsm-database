import json

from tqdm import tqdm

from tables.schemas import ScienceFeedbackTable
from utils import clear_table


def clean(data: dict) -> dict:
    full_data = {}
    flattened = data["flattened_metadata"]
    # Simplify some field names and remove CamelCase
    standard_metadata = {
        "id": flattened["id"],
        "url_id": flattened["hash"],
        "url_content_id": flattened["urlContentId"],
        "claim_reviewed": flattened["claimReviewed"],
        "published_date": flattened["publishedDate"],
        "publisher": flattened["publisher"],
        "review_author": flattened["reviews_author"],
        "review_rating_value": flattened["reviews_reviewRatings_ratingValue"],
        "review_rating_standard_form": flattened["reviews_reviewRatings_standardForm"],
        "url": flattened["url"],
        "normalized_url": flattened["normalized_url"],
        "url_rating_name": flattened["urlReviews_reviewRatings_alternateName"],
        "url_rating_value": flattened["urlReviews_reviewRatings_ratingValue"],
    }
    for k, v in standard_metadata.items():
        if v == "":
            full_data.update({k: None})
        else:
            full_data.update({k: v})
    # When available, add data not in the original CSV
    review_url = (None,)
    if isinstance(data.get("reviews"), list) and len(data["reviews"]) > 0:
        review_url = data["reviews"][0].get("reviewUrl")
    full_data.update(
        {"updated_date": data.get("updatedDate"), "review_url": review_url}
    )
    return full_data


def insert(connection, file):
    table = ScienceFeedbackTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data from De Facto to table: {table.name}\n{file}")
    with open(file, "r") as f:
        data = json.load(f)
        for appearance in tqdm(data, total=len(data)):
            table.insert_values(
                data=clean(appearance),
                connection=connection,
                on_conflict="DO NOTHING",
            )
