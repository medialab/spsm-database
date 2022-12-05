# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

# Collection 1: Misinformation Sources

The collection holds a set of unique URLs, which point to sources of verified misinformation online. The collection is created and updated using the program `merge.py`. The program parses data collected from Condor, Science Feedback, and De Facto and makes the data comptabile with the merged collection. ([Requesting and formatting in CSV new data from Science Feedback and De Facto](https://github.com/medialab/spsm-database#request-new-data)) The program `merge.py` writes its results either to the CSV file `misinformation_sources_<TODAY>.csv` or, if that already exists and to avoid overwriting data, a similar path with a version number appended to the end. In the file, each row corresponds to one source of misinformation online, whose unique identifier (`id`) is a hash of its normalized URL.

To update the collection, use `merge.py`.
 ```shell
 $ python merge.py --dataset [condor|science|defacto] --file <NEW DATA> --length <COUNT OF LINES IN FILE> --collection <PREVIOUSLY COMPILED MERGED COLLECTION>
 ```
### options
1. `--dataset` [required] : `condor`, `science`, or `defacto`
2. `--file` [required] : file path to the dataset containing data you wish to merge into the collection
3. `--length` [optional] : length of the dataset; if provided, it allows for a loading bar
4. `--collection` [optional] : file path to an existing collection, which you wish to update

So as not to overwrite data in an existing collection of misinformation sources, `merge.py` will write results to a different path than that provided with the option `--collection`.

## Dataset Fields: Prefix on Original Fieldname and Mapping to Shared Fields
 ```mermaid
flowchart LR

subgraph condor
    url_rid["condor_url_rid\n(orig. url_rid)"]
    clean_url["condor_clean_url\n(orig. clean_url)"]
    share_title["condor_share_title\n(orig. share_title)"]
    first_post_time["condor_first_post_time\n(orig. first_post_time)"]
    tpfc_rating["condor_tpfc_rating\n(orig. tpfc_rating)"]
    tpfc_first_fact_check["condor_tpfc_first_fact_check\n(orig. tpfc_first_fact_check)"]
    public_shares_top_country["condor_public_shares_top_country\n(orig. public_shares_top_country)"]
end

normalized_url---|normalized|dfurl---|normalized|sfurl---|normalized|clean_url
maindate[date]---datePublished---publishedDate---first_post_time
maintitle[title]---dfclaimReviewed---title---share_title
mainreview[review]---alternateName---urlReviewAlternateName---tpfc_rating

subgraph shared fields
    mainid[id]
    sources
    normalized_url
    normalized_url_hash
    maintitle
    maindate
    mainreview
end

subgraph science feedback
    urlContentId["science_urlContentId\n(orig. urlContentId)"]
    appearanceId["science_appearanceId\n(orig. appearanceId)"]
    sfurl["science_url\n(orig. url)"]
    sfclaimReviewed["science_claimReviewed\n(orig. claimReviewed)"]
    publishedDate["science_publishedDate\n(orig. publishedDate)"]
    publisher["science_publisher\n(orig. publisher)"]
    title["science_title\n(orig. title)"]
    urlReviewAlternateName["science_urlReviewAlternateName\n(orig. urlReviewAlternateName)"]
    urlReviewRatingValue["science_urlReviewRatingValue\n(orig. urlReviewRatingValue)"]
    reviewStandardForm["science_reviewStandardForm\n(orig. reviewStandardForm)"]
    reviewsRatingValue["science_reviewsRatingValue\n(orig. reviewsRatingValue)"]
end

subgraph de facto
    id["defacto_id\n(orig. id)"]
    dfurl["defacto_url\n(orig. url)"]
    dfclaimReviewed["defacto_claimReviewed\n(orig. claimReviewed)"]
    datePublished["defacto_datePublished\n(orig. datePublished)"]
    alternateName["defacto_alternateName\n(orig. alternateName)"]
    themes["defacto_themes\n(orig. themes)"]
    tags["defacto_tags\n(orig. tags)"]
    ratingValue["defacto_ratingValue\n(orig. ratingValue)"]
end
 ```
 

# Request new data
Both programs `defacto.py` (De Facto) and `science.py` (Science Feedback) yield CSV files whose names can be customized with the option `--outfile`. 
By default, the programs' CSV files are titled `defacto_<TODAY>.csv` and `science-feedback_<TODAY>.csv`, respectively, with the day's date in the file name.

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

