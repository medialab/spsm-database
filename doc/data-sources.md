# Data sources

In `src/normalize-data-sources/`, the script [flatten.py](../src/normalize-data-sources/flatten.py) requests, cleans, and formats data from all 3 data sources.

### Table of contents

- [Science Feedback](#science-feedback)
- [Condor](#condor)
- [De Facto](#de-facto)

## Flatten data

To access De Facto and/or Science Feedback's databases, a configuration file with the relevant confidential information is needed.

`config.json`

```json
{
  "science-feedback": {
    "token": "XXXXXXXX-XXXXXXXX",
    "start_date": "2000-01-01",
    "end_date": "2022-12-21",
    "pages": "1000"
  },
  "defacto": {
    "endpoint": "https://XXXXXXXX",
    "end_date": "2022-12-21"
  }
}
```

---

### Science Feedback

When you query the Science Feedback database for every fact-checked item that appeared within a date range (i.e. `--start 2010-01-01` `--end 2022-12-16`), the API returns pages of "appearances". The result of this general search request has the following data format:

#### Appearance requested via date range

```python
{
        "id": "TL74M",
        "publishedDate": "2022-10-29T20:22:35Z",
        "updatedDate": "2022-12-07T09:03:24.396934Z",
        "url": "https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html",
        "urlContentId": "T9744"
    },
```

The appearance results are saved to a folder. Then, while looping through all the results in all the files in that folder, the script parses the ID and requests data on each specific appearance. The result has the following data format:

#### Appearance requested via ID

```python
{'claimReviewed': 'COVID-19 vaccines are linked to abnormal blood clotting, '
                  'sudden deaths, world depopulation',
 'id': 'TL74M',
 'publishedDate': '2022-10-29T20:22:35Z',
 'publisher': None,
 'reviews': [{'author': 'Health Feedback',
              'reviewRatings': [{'alternateName': 'Incorrect',
                                 'bestRating': 5,
                                 'ratingValue': 1.0,
                                 'standardForm': 'Incorrect',
                                 'worstRating': 1}],
              'reviewUrl': 'https://healthfeedback.org/claimreview/the-film-died-suddenly-rehashes-debunked-claims-conspiracy-theories-covid-19-vaccines/'}],
 'updatedDate': '2022-12-07T09:03:24.396934Z',
 'url': 'https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html',
 'urlReviews': [{'reviewRatings': [{'alternateName': 'False',
                                    'bestRating': 5,
                                    'ratingValue': 1.0,
                                    'worstRating': 1}]}]}
```

Finally, that requested data is parsed and certain fields are flattened in a CSV file with the following columns:

| id    | hash                             | normalized_url                                                                 | urlContentId | url                                                                                    | claimReviewed                                                                                | publishedDate        | publisher | reviews_author  | reviews_reviewRatings_ratingValue | reviews_reviewRatings_standardForm | urlReviews_reviewRatings_alternateName | urlReviews_reviewRatings_ratingValue |
| ----- | -------------------------------- | ------------------------------------------------------------------------------ | ------------ | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------- | --------- | --------------- | --------------------------------- | ---------------------------------- | -------------------------------------- | ------------------------------------ |
| TL74M | 4c1c97346dd51aa32218c81bf2df45d6 | rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html | T9744        | https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html | "COVID-19 vaccines are linked to abnormal blood clotting, sudden deaths, world depopulation" | 2022-10-29T20:22:35Z |           | Health Feedback | 1.0                               | Incorrect                          | False                                  | 1.0                                  |

---

### Condor

The Condor dataset is already flattened to a CSV. The flattening script simply enriches it by adding a column with the normalized version of the row's `clean_url` and a column with the hash of that normalized URL.

| url_rid         | hash                             | normalized_url                  | clean_url                                   | first_time_post         | share_title                                                                                          | tpfc_rating           | tpfc_first_fact_check   | public_shares_top_country |
| --------------- | -------------------------------- | ------------------------------- | ------------------------------------------- | ----------------------- | ---------------------------------------------------------------------------------------------------- | --------------------- | ----------------------- | ------------------------- |
| tqyasrlx8u5etbv | b48fdf3a326b18ba32dda6bc81829164 | youtube.com/watch?v=B_5Wk10dO-Q | https://www.youtube.com/watch?v=B_5Wk10dO-Q | 2021-04-09 06:40:00.000 | "BREAKING NEWS TODAY APRIL 9, 2021 PRES DUTERTE TINAWAGAN SI MARCOS PINAUPO SA MALACANANG LENI IYAK" | fact checked as false | 2021-04-14 02:10:00.000 | PH                        |

---

### De Facto

When you query the De Facto database, there is no way to specify a date range. The API returns all fact-checked articles, each with the following format:

#### De Facto fact-check

```python
{
        "id": "Medias/Factuel/Fact-checks/Non-un-arrete-n-autorise-pas-des-pedocriminels-a-devenir-assistants-maternels",
        "title": "Non, un arr\u00eat\u00e9 n'autorise pas \"des p\u00e9docriminels\" \u00e0 devenir \"assistants maternels\"",
        "link": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Non-un-arrete-n-autorise-pas-des-pedocriminels-a-devenir-assistants-maternels/",
        "channel": {
            "id": "Medias/Factuel",
            "name": "Factuel - AFP",
            "url": "https://factuel.afp.com/"
        },
        "chapeau": "<p...</p>",
        "published": "2022-12-09T09:29:19.82+01:00",
        "authors": "XXXXXXXXXXX",
        "themes": [
            "Politique",
            "Soci\u00e9t\u00e9"
        ],
        "tags": [
            "France"
        ],
        "medias": [
            {
                "url": "https://defacto-observatoire.fr/download/Medias/Factuel/Fact-checks/Non-un-arrete-n-autorise-pas-des-pedocriminels-a-devenir-assistants-maternels/WebHome/0599d2e7818664e9750e1d01e6a34fa5a3ee993c-ipad.jpg?rev=1.1"
            }
        ],
        "claim-review": {
            "@context": "https://schema.org",
            "@type": "ClaimReview",
            "url": "https://defacto-observatoire.fr/Medias/Factuel/Fact-checks/Non-un-arrete-n-autorise-pas-des-pedocriminels-a-devenir-assistants-maternels/",
            "datePublished": "2022-12-09T09:29:19.82+01:00",
            "author": {
                "type": "Organization",
                "name": "XXXXXXXXXXX"
            },
            "claimReviewed": "Le contr\u00f4le du FIJAIS n'est plus exig\u00e9 pour l'agr\u00e9ment d'assistant maternel",
            "itemReviewed": {
                "@type": "Claim",
                "author": {
                    "@type": "Person",
                    "name": "Sources multiples"
                },
                "datePublished": "2022-12-03T00:00:00.00+01:00",
                "appearance": {
                    "url": "https://twitter.com/RomanAude/status/1599114199145193472",
                    "headline": ""
                }
            },
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": "1",
                "bestRating": "5",
                "worstRating": "1",
                "alternateName": "Faux"
            }
        },
        "original-url": "https://factuel.afp.com/doc.afp.com.32ZB7NR",
        "body": "<div><p>...</p>"
    },
```

The script parses the publication date of the returned items and filters out all those added to the database after the cut-off date (2022-12-21). Then, the script selects certain data fields and flattens then into a CSV file with the following columns:

| id                                                                                                       | hash                             | normalized_url                                   | themes             | tags   | claim-review_claimReviewed                                                  | claim-review_itemReviewed_datePublished | claim-review_itemReviewed_appearance_url                 | claim-review_itemReviewed_appearance_headline | claim-review_reviewRating_ratingValue | claim-review_reviewRating_alternateName |
| -------------------------------------------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------ | ------------------ | ------ | --------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------- | --------------------------------------------- | ------------------------------------- | --------------------------------------- |
| Medias/Factuel/Fact-checks/Non-un-arrete-n-autorise-pas-des-pedocriminels-a-devenir-assistants-maternels | 543bf6a13f5037f6a40d8d998f6e47b4 | twitter.com/RomanAude/status/1599114199145193472 | Politique\|Société | France | Le contrôle du FIJAIS n'est plus exigé pour l'agrément d'assistant maternel | 2022-12-03T00:00:00.00+01:00            | https://twitter.com/RomanAude/status/1599114199145193472 |                                               | 1                                     | Faux                                    |
