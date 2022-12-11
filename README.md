# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

When downloading this repository, create a virtual Python environment with the packages `click`, `minet`, `requests`, and `ural`.

# Collection 1: Misinformation Sources

A collection of unique URLs, which point to sources of verified misinformation online.

 ```shell
 $ python merge.py --dataset [condor|science|defacto] --filepath PATH/TO/DATA.csv --length INTEGER --merged-table PATH/TO/EXISTING/MERGED-TABLE.csv
 ```
### options
1. `--dataset` [required] : `condor`, `science`, or `defacto`
2. `--filepath` [required] : path to the data you wish to merge into the table
3. `--length` [optional] : length of the data file (if provided, it allows for a loading bar)
4. `--merged-table` [optional] : path to the merged table you wish to update

The merged table preserves every column from the incoming dataset (see Supporting Datasets below) and aggregates data by the URL's normalization.

Cases
- If two or more datasets contain the same URL, their data is written to the same row and in the dataset's dedicated columns.

    |url_id|sources|normalized_url|...|condor_url_rid|...|science_url|...|
    |--|--|--|--|--|--|--|--|
    |4c1c97346dd51aa32218c81bf2df45d6|science\|condor|rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html|...|https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st|...|https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html|

- If a dataset registers a URL under multiple IDs (i.e. Science Feedback reports multiple appearances of the same URL), the data is aggregated in one row.

    |url_id|sources|...|science_id|science_urlContentId|...|
    |--|--|--|--|--|--|
    |d647d2b6e990e637db472c6262cbd7b7|science|...|TL74M\|TL74K|T9744\|T9744|





# Supporting Datasets
To access De Facto and/or Science Feedback's databases, update the configuration file with the relevant confidential information.

`config.json`
```json
{
    "science-feedback":{
        "token": "XXXXXXXX-XXXXXXXX"
    },
    "defacto": {
        "endpoint": "https://XXXXXXXX"
    }
}
```
---

## **Science Feedback**
### Step 1. Request appearances within a date range
When you query the database for all appearances published within a date range (i.e. `--start 2010-01-01` `--end 2010-12-31`), the API returns pages of results. The Click command `request` calls a certain number of those pages (i.e. `--pages 50` ), wherein each page contains a maximum of 100 results matching the query.


```shell
$ python science.py [CONFIG.json] request --start [YYYY-MM-DD] --end [YYYY-MM-DD] --pages [INT]
```

### Step 2. Request information about appearances and flatten to CSV
The Click command `flatten` reads all the appearances previously requested and saved to the default folder. For each appearance, the command requests extra information and flattens that data into a CSV.
```shell
$ python science.py [CONFIG.json] flatten
```

### Appearance requested with the command `request`:
```python
{
        "id": "TL74M",
        "publishedDate": "2022-10-29T20:22:35Z",
        "updatedDate": "2022-12-07T09:03:24.396934Z",
        "url": "https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html",
        "urlContentId": "T9744"
    },
```

### Extra information about the appearance, requested and parsed in the command `flatten`
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

### Flattend CSV of information about the appearance [OUTPUT]
|id|urlContentId|url|claimReviewed|publishedDate|publisher|reviews_author|reviews_reviewRatings_ratingValue|reviews_reviewRatings_standardForm|urlReviews_reviewRatings_alternateName|urlReviews_reviewRatings_ratingValue|
|--|--|--|--|--|--|--|--|--|--|--|
TL74M|T9744|https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html|"COVID-19 vaccines are linked to abnormal blood clotting, sudden deaths, world depopulation"|2022-10-29T20:22:35Z||Health Feedback|1.0|Incorrect|False|1.0

---

## **Condor**
The Condor dataset is already flattened to a CSV and can be immediately incorporated.

|url_rid|clean_url|first_time_post|share_title|tpfc_rating|tpfc_first_fact_check|public_shares_top_country|
|--|--|--|--|--|--|--|
tqyasrlx8u5etbv|https://www.youtube.com/watch?v=B_5Wk10dO-Q|2021-04-09 06:40:00.000|"BREAKING NEWS TODAY APRIL 9, 2021 PRES DUTERTE TINAWAGAN SI MARCOS PINAUPO SA MALACANANG LENI IYAK"|fact checked as false|2021-04-14 02:10:00.000|PH|

---
## **De Facto**
### Step 1. Request and flatten data

Call the function `defacto.py` and provide a path to the configuration file.

```shell
$ python defacto.py [CONFIG.json]
```
### Flattened CSV
|id|themes|tags|claim-review_claimReviewed|claim-review_itemReviewed_datePublished|claim-review_itemReviewed_appearance_url|claim-review_itemReviewed_appearance_headline|claim-review_reviewRating_ratingValue|claim-review_reviewRating_alternateName|
|--|--|--|--|--|--|--|--|--|
|Medias/Factuel/Fact-checks/Non-un-arrete-n-autorise-pas-des-pedocriminels-a-devenir-assistants-maternels|Politique\|Société|France|Le contrôle du FIJAIS n'est plus exigé pour l'agrément d'assistant maternel|2022-12-03T00:00:00.00+01:00|https://twitter.com/RomanAude/status/1599114199145193472||1|Faux|

### JSON response from database
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