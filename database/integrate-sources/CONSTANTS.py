from collections import namedtuple

SCIENCE_FIELDS = ['id', 'hash', 'normalized_url', 'urlContentId', 'url', 'claimReviewed', 'publishedDate', 'publisher', 'reviews_author', 'reviews_reviewRatings_ratingValue', 'reviews_reviewRatings_standardForm', 'urlReviews_reviewRatings_alternateName', 'urlReviews_reviewRatings_ratingValue']

DEFACTO_FIELDS = ['id', 'hash', 'normalized_url', 'themes', 'tags', 'claim-review_claimReviewed', 'claim-review_itemReviewed_datePublished', 'claim-review_itemReviewed_appearance_url', 'claim-review_itemReviewed_appearance_headline', 'claim-review_reviewRating_ratingValue', 'claim-review_reviewRating_alternateName']

DateFormat = namedtuple('DateFormat', ['science_feedback', 'defacto', 'condor', 'condor_review'])

DATE_FORMAT = DateFormat(
    science_feedback="%Y-%m-%dT%H:%M:%S%z",
    defacto="%Y-%m-%dT%H:%M:%S.%f%z",
    condor="%Y-%m-%d %H:%M:%S.%f",
    condor_review="%Y-%m-%dT%H:%M:%S.%f%z"
)
