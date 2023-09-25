import json

from tqdm import tqdm

from table_schemas.de_facto import DeFactoDatasetTable
from table_schemas.utils import clear_table


def clean(data: dict) -> dict:
    flattened_metadata = data["flattened_metadata"]
    claimreview = data["claim-review"]
    full_data = {
        "id": data["id"],
        "normalized_claim_url_hash": flattened_metadata["hash"],
        "normalized_claim_url": flattened_metadata["normalized_url"],
        "themes": data["themes"],
        "tags": data["tags"],
        "review_url": data["claim-review"]["url"],
        "review_publication_date": claimreview["datePublished"],
        "review_author": claimreview["author"].get("name"),
        "claim": flattened_metadata["claim-review_claimReviewed"],
        "claim_url": flattened_metadata["claim-review_itemReviewed_appearance_url"],
        "claim_publication_date": flattened_metadata[
            "claim-review_itemReviewed_datePublished"
        ],
        "claim_url_type": claimreview["itemReviewed"]["appearance"].get("@type"),
        "claim_title": claimreview["itemReviewed"]["appearance"]["headline"],
        "claim_rating_value": flattened_metadata[
            "claim-review_reviewRating_ratingValue"
        ],
        "claim_rating_name": flattened_metadata[
            "claim-review_reviewRating_alternateName"
        ],
    }
    for k, v in full_data.items():
        if v == "":
            v = None
        elif isinstance(v, str):
            v = v.strip()
        full_data.update({k: v})
    return full_data


def insert(connection, dataset):
    table = DeFactoDatasetTable()
    clear_table(connection=connection, table=table)
    print(f"\nImporting data to table: {table.name}\n{dataset}")
    with open(dataset, "r") as f:
        defacto_data = json.load(f)
        for clam_review in tqdm(defacto_data, total=len(defacto_data)):
            table.insert_values(
                data=clean(clam_review),
                connection=connection,
                on_conflict="DO NOTHING",
            )

    return table
