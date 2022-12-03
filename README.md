# SPSM Project Database Manager

Tools to update and modify the SPSM project database's CSV files.

# Request new data
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

Both programs `defacto.py` (De Facto) and `science.py` (Science Feedback) yield CSV files whose names can be customized with the option `--outfile`. 
By default, the programs' CSV files are titled `defacto_<DATE>.csv` and `science-feedback_<DATE>.csv`, respectively, with the day's date in the file name.

## De Facto
The program `defacto.py` sends a request to the De Facto database's endpoint, parses the response, and writes import data to a CSV file.
```shell
$ python defacto.py config.json
```
The file has the following columns: `["id", "themes", "tags", "datePublished", "url", "ratingValue", "alternateName"]`


## Science Feedback
Before the program `science.py` can create a new CSV file of data from Science Feedback, first call pages of appearances and store each 
response in a directory as a JSON file. Large quantities of appearances can be called by appending Science Feedback API's URL parameters 
to the endpoint `api.feedback.org/appearances?`. The appearances will have 5 fields.

`appearances/page_1.json`
```json
[{
    "id": "FOO",
    "publishedDate": "2020-04-06T12:25:29Z",
    "updatedDate": "2021-02-12T14:30:29Z",
    "url": "<https://www.url.com/>",
		"urlContentId": "ZP6Q"
},
{
    "id": "BAR",
    "publishedDate": "2020-03-08T19:53:26Z",
    "updatedDate": "2020-01-01T14:30:29Z",
    "url": "<https://www.second-url.com>",
		"urlContentId": "AAE3"
}]
```

The program `science.py` will loop through the directory of appearances, so the first positional argument is the path to that directory. 
The second positional argument is the configuration file.

```shell
$ python science.py appearances/ config.json
```

Using the token and the endpoint `api.feedback.org/appearances/content/`, the program will call the Science Feedback's API to get key data 
about each appearance, including its title and rating. It will write this data to a CSV file with the following columns:

`["urlContentId", "appearanceId", "claimReviewed", "publishedDate", "publisher", "url", "title", "urlReviewAlternateName", "urlReviewRatingValue", "reviewsStandardForm", "reviewsRatingValue"]`



