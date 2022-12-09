# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

When downloading this repository, create a virtual Python environment with the packages `click`, `minet`, `requests`, and `ural`.

# Collection 1: Misinformation Sources

The collection holds a set of unique URLs, which point to sources of verified misinformation online. The collection is created and updated using the program `merge.py`. The program parses data collected from Condor, Science Feedback, and De Facto and makes the data comptabile with the merged collection. ([Requesting and flattening to CSV new data from Science Feedback and De Facto](https://github.com/medialab/spsm-database#supporting-datasets))

To update the collection, use `merge.py`.
 ```shell
 $ python merge.py --dataset [condor|science|defacto] --file <NEW DATA> --length <COUNT OF LINES IN FILE> --collection <PREVIOUSLY COMPILED MERGED COLLECTION>
 ```
### options
1. `--dataset` [required] : `condor`, `science`, or `defacto`
2. `--file` [required] : file path to the dataset containing data you wish to merge into the collection
3. `--length` [optional] : length of the dataset; if provided, it allows for a loading bar
4. `--collection` [optional] : file path to an existing collection, which you wish to update



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

|id|themes|tags|claim-review_claimReviewed|claim-review_itemReviewed_datePublished|claim-review_itemReviewed_appearance_url|claim-review_itemReviewed_appearance_headline|claim-review_reviewRating_ratingValue|claim-review_reviewRating_alternateName|
|--|--|--|--|--|--|--|--|--|
|Medias/Factuel/Fact-checks/Non-un-arrete-n-autorise-pas-des-pedocriminels-a-devenir-assistants-maternels|Politique\|Société|France|Le contrôle du FIJAIS n'est plus exigé pour l'agrément d'assistant maternel|2022-12-03T00:00:00.00+01:00|https://twitter.com/RomanAude/status/1599114199145193472||1|Faux|
