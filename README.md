# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

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
yields columns: `["id", "themes", "tags", "datePublished", "url", "ratingValue", "alternateName"]`

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

