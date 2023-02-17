from minet.utils import md5
from ural import normalize_url
from datetime import datetime
from CONSTANTS import DATE_FORMAT

class ClaimData:
    def __init__(self, claim):
        self.id = claim.get("id")
        self.themes = "|".join(claim.get("themes"))
        self.tags = "|".join(claim.get("tags"))
        self.claimReviewed = None
        self.reviewPublished = None
        self.datePublished = None
        self.url = None
        self.hash = None
        self.headline = None
        self.ratingValue = None
        self.alternateName = None

        if claim.get("published"):
            self.reviewPublished = datetime.strptime(claim['published'], DATE_FORMAT.condor_review)

        if claim.get("claim-review"):
            self.claimReviewed = claim["claim-review"].get("claimReviewed")
            if claim["claim-review"].get("itemReviewed"):
                self.url = claim["claim-review"]["itemReviewed"]["appearance"].get("url")
                self.normalized_url = normalize_url(self.url)
                self.hash = md5(self.normalized_url)
                self.headline = claim["claim-review"]["itemReviewed"]["appearance"].get("headline")
                if claim["claim-review"]["itemReviewed"].get("datePublished"):
                    unformatted_date = claim["claim-review"]["itemReviewed"]["datePublished"]
                    self.datePublished = datetime.strptime(unformatted_date, DATE_FORMAT.defacto)

        if claim.get("claim-review") and claim["claim-review"].get("reviewRating"):
            self.ratingValue = claim["claim-review"]["reviewRating"].get("ratingValue")
            self.alternateName = claim["claim-review"]["reviewRating"].get("alternateName")

    def mapping(self):
        return {
            "id":self.id,
            "hash":self.hash,
            "normalized_url":self.normalized_url,
            "themes":self.themes,
            "tags":self.tags,
            "claim-review_claimReviewed":self.claimReviewed,
            "claim-review_itemReviewed_datePublished":self.datePublished,
            "claim-review_itemReviewed_appearance_url":self.url,
            "claim-review_itemReviewed_appearance_headline":self.headline,
            "claim-review_reviewRating_ratingValue":self.ratingValue,
            "claim-review_reviewRating_alternateName":self.alternateName
        }
