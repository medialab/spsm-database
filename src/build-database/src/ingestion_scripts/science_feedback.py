import json

from tqdm import tqdm

from table_schemas.science import ScienceFeedbackDatasetTable
from table_schemas.utils import clear_table
from table_schemas.enriched_titles import (
    add_enriched_titles,
    setup_enriched_title_dataset_table,
)


def clean(data: dict) -> dict:
    full_data = {}
    flattened = data["flattened_metadata"]
    # Simplify some field names and remove CamelCase
    standard_metadata = {
        "id": flattened["id"],
        "normalized_claim_url_hash": flattened["hash"],
        "url_content_id": flattened["urlContentId"],
        "claim_reviewed": flattened["claimReviewed"],
        "published_date": flattened["publishedDate"],
        "publisher": flattened["publisher"],
        "review_author": flattened["reviews_author"],
        "review_rating_value": flattened["reviews_reviewRatings_ratingValue"],
        "review_rating_standard_form": flattened["reviews_reviewRatings_standardForm"],
        "url": flattened["url"],
        "normalized_claim_url": flattened["normalized_url"],
        "url_rating_name": flattened["urlReviews_reviewRatings_alternateName"],
        "url_rating_value": flattened["urlReviews_reviewRatings_ratingValue"],
    }
    for k, v in standard_metadata.items():
        if v == "":
            v = None
        elif isinstance(v, str):
            v = v.strip()
        full_data.update({k: v})

    # Synthesize the fact-check rating, prioritizing the review rating
    full_data.update({"review_or_url_rating_value": None})
    if full_data.get("review_rating_value"):
        full_data["review_or_url_rating_value"] = full_data["review_rating_value"]
    elif full_data.get("url_rating_value"):
        full_data["review_or_url_rating_value"] = full_data["url_rating_value"]

    # When available, add data from the enriched JSON (aka not in the original CSV)
    review_url = (None,)
    if isinstance(data.get("reviews"), list) and len(data["reviews"]) > 0:
        review_url = data["reviews"][0].get("reviewUrl")
    full_data.update(
        {"updated_date": data.get("updatedDate"), "review_url": review_url}
    )
    return full_data


def insert(connection, dataset, supplemental_titles):
    table = ScienceFeedbackDatasetTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data to table: {table.name}\n{dataset}")
    with open(dataset, "r") as f:
        data = json.load(f)
        for appearance in tqdm(data, total=len(data)):
            table.insert_values(
                data=clean(appearance),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    # Enrich the Science Feedback dataset table with titles
    setup_enriched_title_dataset_table(
        connection=connection, dataset=supplemental_titles
    )
    print(f"\nAltering the table {table.name} to have columns for enriched titles.")
    add_enriched_titles(
        connection=connection,
        target_url_id_col_name="normalized_claim_url_hash",
        target_table=table,
    )
    return table
