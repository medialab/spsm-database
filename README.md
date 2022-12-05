# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

# Collection 1: Misinformation Sources

The collection of misinformation sources holds a set of unique URLs, which point to sources of verified misinformation online. The collection is created and updated using the program `merge.py`. The program parses data from Condor, Science Feedback, or De Facto and makes the data comptabile with the merged collection.

The first time `merge.py` adds a new source of misinformation to the collection, the shared fields `url`, `date`, `title`, and `review` are populated with data mapped from the original dataset. In addition to mapping data, each new entry also has the created fields `sources`, `normalized_url`, and `normalized_url_hash`. The normalized URL and its hash protect against duplicates and provide a unique ID for each source, respectively.

If two different datasets have the same URL, fields from the second dataset are added to the collection if the second dataset has not already contributed to information about that particular source of misinformation. The `sources` field is then updated to include the second dataset. Multiple datasets are concatenated in the `sources` field using a pipe, i.e. "`condor|science`".

While only a portion of a dataset's data is mapped to shared fields in the collection, the collection of misinformation nevertheless preserves the original data. To all the original fieldnames, the program `merge.py` adds a prefix signifying the relevant dataset. The program then reproduces the original data in the dataset's relevant column. For example, while Science Feedback's field `title` is both mapped to the shared field `title` and reproduced in the field `science_title`, data from Science Feedback's field `claimReveiwed`, which is not mapped to a shared field, is nevertheless preserved in the collection's field `science_claimReviewed`. All data data fields in the diagram below are preserved in the collection.

 ```mermaid
flowchart LR

subgraph condor
    url_rid
    clean_url
    share_title
    first_post_time
    tpfc_rating
    tpfc_first_fact_check
    public_shares_top_country
end

mainurl[url]---dfurl---sfurl---clean_url
maindate[date]---datePublished---publishedDate---first_post_time
maintitle[title]---dfclaimReviewed---title---share_title
mainreview[review]---alternateName---urlReviewAlternateName---tpfc_rating

subgraph shared fields
    mainid[id]
    sources
    maintitle
    mainurl
    maindate
    mainreview
end

subgraph science feedback
    urlContentId
    appearanceId
    sfurl[url]
    sfclaimReviewed[claimReviewed]
    publishedDate
    publisher
    title
    urlReviewAlternateName
    urlReviewRatingValue
    reviewStandardForm
    reviewsRatingValue
end

subgraph de facto
    id
    dfurl[url]
    dfclaimReviewed[claimReviewed]
    datePublished
    alternateName
    themes
    tags
    ratingValue
end
 ```


# Request new data
Both programs `defacto.py` (De Facto) and `science.py` (Science Feedback) yield CSV files whose names can be customized with the option `--outfile`. 
By default, the programs' CSV files are titled `defacto_<DATE>.csv` and `science-feedback_<DATE>.csv`, respectively, with the day's date in the file name.

A JSON configuration file must provide credentials necessary to request data from De Facto and Science Feedback. De Facto's database is accessed with 
a protected endpoint. Science Feedback's API requires a token. Provide both of these data in the JSON configuration file.

`config.json`
```json
{
    "science-feedback":{
        "token": "TOKEN",
        "endpoint": "https://api.feedback.org/appearances/content/"
    },
    "defacto":"ENDPOINT"
}
```
---

## De Facto
```shell
$ python defacto.py config.json
```
yields columns: `["id", "claimReviewed", "themes", "tags", "datePublished", "url", "ratingValue", "alternateName"]`

---

## Science Feedback
```shell
$ python science.py appearances/ config.json
```
yields columns: `["urlContentId", "appearanceId", "claimReviewed", "publishedDate", "publisher", "url", "title", "urlReviewAlternateName", "urlReviewRatingValue", "reviewsStandardForm", "reviewsRatingValue"]`

### *Note*

*`science.py` loops through a directory of saved responses from Science Feedback's API. To populate this directory with the right kind of data, 
call pages of appearances from Science Feedback's API and store each response as a JSON file. Large quantities of appearances can be called from Science Feedback's database by appending parameters to the API's endpoint. Below is an example of how to request pages of appearances and save each page to a file in a directory, i.e. `./appearances/`.*

```shell
TOKEN="..."

i=0
startPublishedDate="2000-01-01"
endPublishedDate="2022-12-01"

mkdir -p appearances

while [ $i -le 50 ]
do
    curl -H "X-Access-Tokens: ${TOKEN}" "api.feedback.org/appearances?page=${i}&paginator=100&startPublishedDate=${startPublishedDate}&endPublishedDate=${endPublishedDate}" > appearances/page_${i}.json
    ((i++))
done
```
---

