# Collection 1: Misinformation Sources

## Merge Data

Merge data from the 3 data sources into one meta table, which aggregates data by URL.

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

## Archive Web Pages

From the merged table, select the 1st (`url_id`) and 3rd column (`normalized_url`) as the archived web page's identifying hash and its URL, respectively. 

|url_id|sources|normalized_url|...|
|--|--|--|--|
|4c1c97346dd51aa32218c81bf2df45d6|...|rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html|...|

Objective:
- Download the HTML and source files for each web page.
- Enrich the merged table with the following columns:
    - `archive_timestamp` : the time at which `wget` downloaded the HTML,
    - default columns added with `minet` CLI command `fetch`.
