from datetime import datetime
from CONSTANTS import DATE_FORMAT

from minet.utils import md5
from ural import normalize_url

class AppearanceData:
    def __init__(self, data):
        self.claimReviewed = data.get("claimReviewed")
        self.id = data.get("id")
        self.publishedDate = None
        self.publisher = data.get("publisher")
        self.url = data.get("url")
        self.normalized_url = normalize_url(self.url)
        self.hash = md5(self.normalized_url)
        self.reviews_author = None
        self.reviews_reviewRatings_ratingValue = None
        self.reviews_reviewRatings_standardForm = None
        self.urlReviews_reviewRatings_alternateName = None
        self.urlReviews_reviewRatings_ratingValue = None
        self.urlContentId = None

        if data.get("publishedDate"):
            self.publishedDate = datetime.strptime(data['publishedDate'], DATE_FORMAT.science_feedback)

        reviews = data.get("reviews")
        if reviews:
            self.reviews_author = reviews[0].get("author")
            if reviews[0].get("reviewRatings"):
                self.reviews_reviewRatings_ratingValue = reviews[0].get("reviewRatings")[0].get("ratingValue")
                self.reviews_reviewRatings_standardForm = reviews[0].get("reviewRatings")[0].get("standardForm")
        urlReviews = data.get("urlReviews")
        if urlReviews and urlReviews[0].get("reviewRatings"):
            self.urlReviews_reviewRatings_alternateName = urlReviews[0].get("reviewRatings")[0].get("alternateName")
            self.urlReviews_reviewRatings_ratingValue = urlReviews[0].get("reviewRatings")[0].get("ratingValue")

    def mapping(self, urlContentId:str):
        return {
            "id":self.id,
            "urlContentId":urlContentId,
            "hash":self.hash,
            "claimReviewed":self.claimReviewed,
            "publishedDate":self.publishedDate,
            "publisher":self.publisher,
            "reviews_author":self.reviews_author,
            "reviews_reviewRatings_ratingValue":self.reviews_reviewRatings_ratingValue,
            "reviews_reviewRatings_standardForm":self.reviews_reviewRatings_standardForm,
            "url":self.url,
            "normalized_url":self.normalized_url,
            "urlReviews_reviewRatings_alternateName":self.urlReviews_reviewRatings_alternateName,
            "urlReviews_reviewRatings_ratingValue":self.urlReviews_reviewRatings_ratingValue
        }
