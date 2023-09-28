# from flatten_sciencefeedback import AppearanceData
import csv
import casanova
import json
from collections import Counter
from flatten_sciencefeedback import AppearanceData
from pathlib import Path


aggregated_urls = "/Users/kelly.christensen/Dev/spsm/spsm-data/url_table.csv"
flattened_science_feedback = (
    "/Users/kelly.christensen/Dev/spsm/spsm-data/sources/sf_flattened_2022-12-22_1.csv"
)
outfile = "hard_coded_full_science_feedback.csv"
downloaded_appearances = "/Users/kelly.christensen/Dev/spsm/spsm-data/sources/science_feedback_appearances_2022-12-22"
downloaded_appearance_metadata = "/Users/kelly.christensen/Dev/spsm/spsm-data/database-files/for_import/science_feedback_full.json"

if __name__ == "__main__":
    index = {}
    with casanova.reader(flattened_science_feedback) as reader:
        if reader.headers:
            # ID of the claim appearance
            id_pos = reader.headers["id"]

            # Hash of the claim appearance's URL
            url_id_pos = reader.headers["hash"]

            # Normalized version of the claim appearance's URL
            normalized_url_pos = reader.headers["normalized_url"]

            # Science Feedback's unique identifier for the content/URL of the claim,
            # which may make multiple appearances in the database
            urlContentId_pos = reader.headers["urlContentId"]

            # Claim appearance's URL
            url_pos = reader.headers["url"]

            # What is claimed in the appearance
            claimReviewed_pos = reader.headers["claimReviewed"]

            # Publication of the claim appearance online
            publishedDate_pos = reader.headers["publishedDate"]

            # Declared publisher of the claim appearance
            publisher_pos = reader.headers["publisher"]

            # Author of the first review of the claim appearance (e.g. Politico)
            reviews_author_pos = reader.headers["reviews_author"]

            # Ratings given to the first review of the claim appearance
            reviews_reviewRatings_ratingValue_pos = reader.headers[
                "reviews_reviewRatings_ratingValue"
            ]
            reviews_reviewRatings_standardForm_pos = reader.headers[
                "reviews_reviewRatings_standardForm"
            ]

            # Ratings given to all appearances in the database of this URL
            urlReviews_reviewRatings_alternateName_pos = reader.headers[
                "urlReviews_reviewRatings_alternateName"
            ]
            urlReviews_reviewRatings_ratingValue_pos = reader.headers[
                "urlReviews_reviewRatings_ratingValue"
            ]

            for row, id in reader.cells("id", with_rows=True):
                if row[url_id_pos] == "32c65045b5a3fbd0cce98315caf21a82":
                    print("FOUND IT!")
                index.update(
                    {
                        id: {
                            "claim_appearance_id": row[id_pos],
                            "claim_url": row[url_pos],
                            "normalized_claim_url": row[normalized_url_pos],
                            "normalized_claim_url_hash": row[url_id_pos],
                            "claim_reviewed": row[claimReviewed_pos],
                            "claim_publication_date": row[publishedDate_pos],
                            "claim_publisher": row[publisher_pos],
                            "first_claim_appearance_review_author": row[
                                reviews_author_pos
                            ],
                            "first_claim_appearance_review_rating_value": row[
                                reviews_reviewRatings_ratingValue_pos
                            ],
                            "first_claim_appearance_review_rating_standard_form": row[
                                reviews_reviewRatings_standardForm_pos
                            ],
                            "first_claim_appearance_review_url": None,
                            "updated_review_date": None,
                            "claim_url_content_id": row[urlContentId_pos],
                            "claim_url_content_review_rating_value": row[
                                urlReviews_reviewRatings_ratingValue_pos
                            ],
                            "claim_url_content_review_rating_alternate_name": row[
                                urlReviews_reviewRatings_alternateName_pos
                            ],
                        }
                    }
                )

    # Compose new CSV with 2023 appearances that includes a priori all 2022 appearances
    with open(downloaded_appearance_metadata) as f:
        data = json.load(f)

    appearance_id = None

    for appearance in data:
        appearance_id = appearance["flattened_metadata"].get("id")
        d = appearance["flattened_metadata"]
        if d["hash"] == "32c65045b5a3fbd0cce98315caf21a82":
            print("FOUND IT!")
        if not index.get(appearance_id):
            index.update(
                {
                    appearance_id: {
                        "claim_appearance_id": appearance_id,
                        "claim_url": d["url"],
                        "normalized_claim_url": d["normalized_url"],
                        "normalized_claim_url_hash": d["hash"],
                        "claim_reviewed": d["claimReviewed"],
                        "claim_publication_date": d["publisehdDate"],
                        "claim_publisher": d["publisher"],
                        "first_claim_appearance_review_author": d["reviews_author"],
                        "first_claim_appearance_review_rating_value": d[
                            "reviews_reviewRatings_ratingValue"
                        ],
                        "first_claim_appearance_review_rating_standard_form": d[
                            "reviews_reviewRatings_standardForm"
                        ],
                        "first_claim_appearance_review_url": None,
                        "updated_review_date": None,
                        "claim_url_content_id": d["urlContentId"],
                        "claim_url_content_review_rating_value": d[
                            "urlReviews_reviewRatings_ratingValue"
                        ],
                        "claim_url_content_review_rating_alternate_name": d[
                            "urlReviews_reviewRatings_alternateName"
                        ],
                    }
                }
            )
        index[appearance_id].update(
            {"updated_review_date": appearance.get("updatedDate")}
        )
        if appearance.get("reviews"):
            first_review = appearance["reviews"][0]
            index[appearance_id].update(
                {"first_claim_appearance_review_url": first_review.get("reviewUrl")}
            )

    if appearance_id:
        headers = list(index[appearance_id].keys())
        with open(outfile, "w") as of:
            writer = csv.DictWriter(of, headers)
            writer.writeheader()
            for _, v in index.items():
                writer.writerow(v)
