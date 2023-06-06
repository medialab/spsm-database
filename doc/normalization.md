# Data source harmonization

It was desireable to build a CSV file that aggregates all unique URLs in the 3 data sources because this would provide a dataset on which further enrichment of the online content (archiving, web scraping) could be done efficiently. Therefore, a [script](../src/normalize-data-sources/merge.py) aggregated the 3 data sources' URLs and merged the data in one table. The merged table preserves every column from the incoming dataset.

## Special Cases

- If two or more datasets contain the same URL, their data is written to the same row. Each dataset's particular metadata is written to dataset's dedicated columns.

  | url_id                           | sources         | normalized_url                                                                 | ... | condor_url_rid                                                                    | ... | science_url                                                                            | ... |
  | -------------------------------- | --------------- | ------------------------------------------------------------------------------ | --- | --------------------------------------------------------------------------------- | --- | -------------------------------------------------------------------------------------- | --- |
  | 4c1c97346dd51aa32218c81bf2df45d6 | science\|condor | rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html | ... | https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st | ... | https://rumble.com/v1q3s40-died-suddenly-official-trailer-streaming-november-21st.html |

- If one dataset contains a URL under multiple IDs (i.e. Science Feedback reports multiple appearances of the same URL), the data is aggregated in one row.

  | url_id                           | sources | ... | science_id   | science_urlContentId | ... |
  | -------------------------------- | ------- | --- | ------------ | -------------------- | --- |
  | d647d2b6e990e637db472c6262cbd7b7 | science | ... | TL74M\|TL74K | T9744\|T9744         |
