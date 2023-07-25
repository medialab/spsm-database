# Collection on <span dir="">tweet_search_title_23_03</span>

All sources from FR or US or with a web language identified as FR or EN were selected (53,745) from the database. The number of unique titles in that set is 44,778.

The ordering is explained in [the 6th `remove_webpate_title_ending` script](https://gitlab.sciences-po.fr/spsm/spsm/-/blob/main/collection/scripts/remove_webpate_title_ending_6.R#L922), which was applied to the cleaning process for collections as early as 17 March 2023. The cleaning portion of the script was applied to the test collection run on 14 March.

Each item in the selection was then given a number that reflects its priority in the collection process. The numbers range from 1 to 12. The distribution is as follows:
| **order** | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|----|----|----|
| **data source** | Condor | Condor | Condor | Condor | Condor | Science Feedback | Science Feedback | Science Feedback | Science Feedback | Science Feedback | Science Feedback | remainder (De Facto)
| **data field** | `tpfc_rating` | `tpfc_rating` | `tpfc_rating` | `tpfc_rating` | `tpfc_rating` | `reviews`/ `reviewRatings`/ `ratingValue` | `reviews`/ `reviewRatings`/ `ratingValue` | `reviews`/ `reviewRatings`/ `ratingValue` | `reviews`/ `reviewRatings`/ `ratingValue` | `reviews`/ `reviewRatings`/ `ratingValue` | `reviews`/ `reviewRatings`/ `ratingValue` | ---
| **value**   | "fact checked as false" | NULL or other | "fact checked as true" | "not rated" | "not eligible" | 1.0 | 2.0 | 3.0 | 4.0 | 5.0 | NULL | ---
|**total**| 11,377 | 6,159 | 2,117 | 15,059 | 5,049 | 2,933 | 1,266 | 139 | 62 | 113 | 479 | 25 |

## 14 March 2023

### Collection 1 (FINISHED) : Pre-ordering
Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `tweet_search_march_2023/test_first_1_3500_pedro_output`
* key: Pedro
* files
  - `tweet_search_march_2023/datasets/test_first_1_3500.csv` (924 rows)

Results of the collection:

* start time: 2023-03-14 18:56:59
* finish time: 2023-03-15 07:04:19
* errors: 4
  - 2 timeout
  - 0.22% queries timed-out
* results:
  - 999,487 tweets collected
  - 891 (96.4%) returned results
  - <span dir="">\~</span>1,122 tweets per query

Performance of the collection

* duration: 12:07:20
* ratio: 23 tweets / second


## 17 March 2023

### Collection 1 (FINISHED) : Order 1, all

The collection launched on Friday, 17 March took advantage of only 1 API key (Kelly) because it would reset on 19 March.

Parameters of the collection:

- profile: Kelly
- Python environment: `minet3.11`
- script: `single-file_keywordsearch_keep-outfile.py`
- directory: `march17-collection/Order1_KellyKey_output`
- key: Kelly
- files:
  * `title_2023_03_15_fr_en_order1.csv` (9,806 rows without skips)
  * concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order1_index0_clean_IG.csv`(rows 1-1000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index1000_clean_IG.csv` (rows 1001-2000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index2000_clean_IG.csv` (rows 2001-3000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index3000_clean_IG.csv` (rows 3001-4000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index4000_clean_IG.csv` (rows 4001-5000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index5000_clean_IG.csv` (rows 5001-6000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index6000_clean_IG.csv` (rows 6001-7000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index7000_clean_IG.csv` (rows 7001-8000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index8000_clean_IG.csv` (rows 8001-9000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index9000_clean_IG.csv` (rows 9001-10,000)
    * `tweet_search_title_2023_03_15_fr_en_order1_index10000_clean_IG.csv` (rows 10,001-10,544)
  * 833 (11377-10544) items from `order 1` were marked as `done` and therefore not part of the collection's dataset.

Results of the collection:

* start time: 2023-03-17 16:24:20
* finish time: 2023-03-21 18:12:53
* errors: 70
  - 31 timeout
  - 0.36 % queries timed-out
* results:
  - 5,962,927 tweets collected
  - 8,698 queries (82.5%) returned results
  - <span dir="">\~</span>686 tweets per query

Performance of the collection

* duration: 4 days, 1:48:33
* ratio: 17 tweets / second

## 19 March 2023 (FINISHED)

### Collection 1 (FINISHED) : Order 2, Index 0

A collection was launched the weekend on Sunday, 19 March, running on one of the chunks from priority group 2 that had been cleaned by Friday.

Parameters of the collection:

* profile: Achim
* Python environment: ?
* script: `single-file_keywordsearch_keep-outfile.py`
* directory: `march19-collection/Order2_index0_KellyKey_output`
* key: Kelly
* files:
  * `tweet_search_title_2023_03_15_fr_en_order2_index0_clean_IG_skip0.csv` (937 rows)

Results of the collection:

* start time: 2023-03-19 13:41:20
* finish time: 2023-03-20 20:50:34
* errors: 18
  - 14 timeout
  - 1.65% queries timed-out
* results:
  - 641,676 tweets collected
  - 849 queries (90.6%) returned results
  - <span dir="">\~</span>756 tweets per query

Performance of the collection

* duration: 1 day, 7:09:14
* ratio: 6 tweets / second


## March 20 collections

### Collection 1 (FINISHED) : Order 2, Index 1000-3000

Parameters of the collection:

* profile: Kelly
* screen: 342234.pts-0.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march20-collection/Order2_1000-3000_BenjaminKey_output`
* key: Benjamin
* files:
  * `tweet_search_title_2023_03_15_fr_en_order2_index1000-3000_skip0.csv` (2,787 rows, with skips removed)
  * concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order2_index1000_clean_RR.csv`
    * `tweet_search_title_2023_03_15_fr_en_order2_index2000_clean_RR.csv`
    * `tweet_search_title_2023_03_15_fr_en_order2_index3000_clean_RR.csv`

Results of the collection:

* start time: 2023-03-20 12:43:35
* finish time: 2023-03-21 15:09:09
* errors: 8
  - 5 timeout
  - 0.2% queries timed-out
* results:
  - 2,270,972 tweets collected
  - 2,562 queries (92%) returned results
  - <span dir="">\~</span>886 tweets per query

Performance of the collection

* duration: 1 day, 2:25:34
* ratio: 24 tweets / second

### Collection 2 (FINISHED) : Order 2, Index 4000-6000

Parameters of the collection:

* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march20-collection/Order2_4000-6000_output` (forgot to add key to name)
* key: Jean-Philippe
* files:
  * `tweet_search_title_2023_03_15_fr_en_order2_index4000-6000_skip0.csv` (1,935 rows with skips removed)
  * concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order2_index4000_clean_AE.csv`
    * `tweet_search_title_2023_03_15_fr_en_order2_index5000_clean_RR.csv`
    * `tweet_search_title_2023_03_15_fr_en_order2_index6000_clean_AE_RR.csv`
  * 7 items from `order 2` were marked as `done`.

Results of the collection:

* start time: 2023-03-20 15:06:49
* finish time: 2023-03-21 11:58:55
* errors: 11
  - 9 timeout
  - 0.51 % queries timed-out
* results:
  - 1,853,089 tweets collected
  - 1,756 queries (90.8%) returned results
  - <span dir="">\~</span>1,055 tweets per query

Performance of the collection

* duration: 20:52:06
* ratio: 25 tweets / second

### Collection 3 (FINISHED) : Order 3, all

Parameters of the collection:

* profile: Kelly
* screen: 377456.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march20-collection/Order3_PedroKey_output`
* key: Pedro
* files:
  * `tweet_search_title_2023_03_15_fr_en_order3_skip0.csv` (1,997 rows with skips removed)
  * concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order3_index0_clean_AE.csv`
    * `tweet_search_title_2023_03_15_fr_en_order3_index1000_clean_RR.csv`
    * `tweet_search_title_2023_03_15_fr_en_order3_index2000_clean_RR.csv`

Results of the collection:

* start time: 2023-03-20 16:05:38
* finish time: 2023-03-21 09:43:43
* errors: 8
  - 5 timeout
  - 0.27% queries timed-out
* results:
  - 1,629,382 tweets collected
  - 1,857 queries (93%) returned results
  - <span dir="">\~</span>877.4 tweets per query

Performance of the collection

* duration: 17:38:05
* ratio: 26 tweets / second

## March 21 collections

### Collection 1 (FINISHED) : Order 4, Index 0-4000

Parameters of the collection:

* profile: Kelly
* screen: 377456.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march21-collection/Order4_PedroKey_output`
* key: Pedro
* files
  - `tweet_search_title_2023_03_15_fr_en_order4_index0-2000_skip0.csv` (2,527 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order4_index0_clean_RR.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index1000_clean_RR.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index2000_clean_RR.csv` (1,000 rows)

Results of the collection:

* start time: 2023-03-21 11:02:17
* finish time: 2023-03-22 05:06:16
* errors: 18
  - 4 timeout
  - 0.18% queries timed-out
* results:
  - 1,534,124 tweets collected
  - 2,170 queries (85.9%) returned results
  - <span dir="">\~</span>706 tweets per query

Performance of the collection

* duration: 18:03:59
* ratio: 24 tweets / second

### Collection 2 (FINISHED) : Order 4, Index 3000-5000

Parameters of the collection:

* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march21-collection/Order4_JPKey_output`
* key: Jean-Philippe
* files
  - `tweet_search_title_2023_03_15_fr_en_order4_index3000-5000_skip0.csv` (2,505 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order4_index3000_clean_RR.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index4000_clean_RR.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index5000_clean_RR.csv` (1,000 rows)

Results of the collection:

* start time: 2023-03-21 13:13:14
* finish time: 2023-03-22 06:16:28
* errors: 18
  - 3 timeout
  - 0.14% queries timed-out
* results:
  - 1,518,972 tweets collected
  - 2,165 queries (86.4%) returned results
  - <span dir="">\~</span>701 tweets per query

Performance of the collection

* duration: 17:03:14
* ratio: 25 tweets / second

### Collection 3 (FINISHED) : Order 4, Index 6000-8000

Parameters of the collection:

* profile: Kelly
* screen: 342234.pts-0.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march21-collection/Order4_6000-8000_BenjaminKey_output`
* key: Benjamin
* files
  - `tweet_search_title_2023_03_15_fr_en_order4_index6000-8000_skip0.csv` (2,598 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order4_index6000_clean_RR.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index7000_clean_RR.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index8000_clean_RR.csv` (1,000 rows)

Results of the collection:

* start time: 2023-03-21 16:33:57
* finish time: 2023-03-22 17:10:24
* errors: 31
  - 12 timeout
  - 0.53% queries timed-out
* results:
  - 2,213,079 tweets collected
  - 2,253 queries (86.7%) returned results
  - <span dir="">\~</span>982 tweets per query

Performance of the collection

* duration: 1 day, 0:36:27
* ratio: 25 tweets / second

### Collection 4 (FINISHED) : Order 4, Index 9000-10000

Parameters of the collection:

* profile: Kelly
* screen: 377456.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march21-collection/Order4_9000-10000_PedroKey_output`
* key: Pedro
* files
  - `tweet_search_title_2023_03_15_fr_en_order4_index9k-10k_skip0.csv` (1,622 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order4_index9000_clean_RR.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index10000_clean_RR.csv` (1,000 rows)

Results of the collection:

* start time: 2023-03-22 05:06:19
* finish time: 2023-03-22 17:36:59
* errors: 16
  - 2 timeout
  - 0.14% queries timed-out
* results:
  - 1,057,495 tweets collected
  - 1,401 queries (86.4%) returned results
  - <span dir="">\~</span>755 tweets per query

Performance of the collection

* duration: 12:30:40
* ratio: 24 tweets / second

## March 22 collections

### Collection 1 (FINISHED) : Order 4, Index 11000

Parameters of the collection:
* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march22-collection/Order4_11000_JPKey_output`
* key: Jean-Philippe
* files
  - `tweet_search_title_2023_03_15_fr_en_order4_index11000_skip0.csv` (656 rows with skips removed)

Results of the collection:

* start time: 2023-03-22 09:28:46
* finish time: 2023-03-22 14:50:09
* errors: 1
  - 1 timeout
  - 0.18% queries timed-out
* results:
  - 494,004 tweets collected
  - 563 queries (85.8%) returned results
  - <span dir="">\~</span>877 tweets per query

Performance of the collection

* duration: 5:21:23
* ratio: 26 tweets / second


### Collection 2 (FINISHED) : Order 4, Index 12000-13000

Parameters of the collection:
* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march22-collection/Order4_12000-13000_JPKey_output`
* key: Jean-Philippe
* files
  - `tweet_search_title_2023_03_15_fr_en_order4_index12000-13000_skip0.csv` (1,739 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order4_index12000_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index13000_clean_IG.csv` (1,000 rows)

Results of the collection:

* start time: 2023-03-22 15:12:31
* finish time: 2023-03-23 06:27:53
* errors: 7
  - 5 timeout
  - 0.33 % queries timed-out
* results:
  - 1,369,404 tweets collected
  - 1,531 (88%) returned results
  - <span dir="">\~</span>895 tweets per query

Performance of the collection

* duration: 15:15:22
* ratio: 25 tweets / second


### Collection 3 (FINISHED) : Order 5, Index 0-1000

Parameters of the collection:

* profile: Kelly
* screen: 342234.pts-0.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march22-collection/Order5_0-1000_BenjaminKey_output`
* key: Benjamin
* files
  - `tweet_search_title_2023_03_15_fr_en_order5_index0-1000_skip0.csv` (1,015 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order5_index0_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order5_index1000_clean_IG.csv` (1,000 rows)

Results of the collection:

* start time: 2023-03-22 17:57:52
* finish time: 2023-03-23 00:17:29
* errors: 9
  - 4 timeout
  - 0.47% queries timed-out
* results:
  - 568,652 tweets collected
  - 853 (84%) returned results
  - <span dir="">\~</span>667 tweets per query

Performance of the collection

* duration: 6:19:37
* ratio: 25 tweets / second



### Collection 4 (FINISHED) : Order 4, Index 14000-15000

Parameters of the collection:
* profile: Kelly
* screen: 377456.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march22-collection/Order4_index14000-15000_PedroKey_output`
* key: Pedro
* files
  - `tweet_search_title_2023_03_15_fr_en_order4_index14000-15000_skip0.csv` (908 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order4_index14000_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order4_index15000_clean_IG.csv` (59 rows)

Results of the collection:

* start time: 2023-03-22 18:02:32
* finish time: 2023-03-23 00:21:55
* errors: 9
  - 3 timeout
  - 0.42% queries timed-out
* results:
  - 504,897 tweets collected
  - 708 (78%) returned results
  - <span dir="">\~</span>713 tweets per query

Performance of the collection

* duration: 6:19:23
* ratio: 22 tweets / second


## March 23 collections

### Collection 1 (FINISHED) : Order 5, Index 2000-3000

Parameters of the collection:

* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march23-collection/Order5_2000-3000_BenjaminKey_output`
* key: Benjamin
* files
  - `tweet_search_title_2023_03_15_fr_en_order5_index2000-3000_skip0.csv` (1,101 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order5_index2000_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order5_index3000_clean_IG.csv` (1,000 rows)

Results of the collection:

* start time: 2023-03-23 06:50:28
* finish time: 2023-03-23 15:06:58
* errors: 7
  - 6 timeout
  - 0.65% queries timed-out
* results:
  - 773,023 tweets collected
  - 925 (84%) returned results
  - <span dir="">\~</span>836 tweets per query

Performance of the collection

* duration: 8:16:30
* ratio: 26 tweets / second


### Collection 2 (FINISHED) : Order 5, Index 4000-5000

Parameters of the collection:

* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march23-collection/Order5_4000-5000_BenjaminKey_output`
* key: Benjamin
* files
  - `tweet_search_title_2023_03_15_fr_en_order5_index4000-5000_skip0.csv` (569 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order5_index4000_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order5_index5000_clean_IG.csv` (49 rows)

Results of the collection:

* start time: 2023-03-23 15:07:00
* finish time: **unknown**
* errors: 1
  - 1 timeout
  - 0.21% queries timed-out
* results:
  - 289,875 tweets collected
  - 470 (82.6%) returned results
  - <span dir="">\~</span>617 tweets per query

Performance of the collection

* duration: **unknown**
* ratio: **unknown** tweets / second


### Collection 3 (FINISHED) : Order 6, Index 0-2000

Parameters of the collection:

* profile: Kelly
* screen: 377456.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march23-collection/Order6_0-2000_PedroKey_output`
* key: Pedro
* files
  - `tweet_search_title_2023_03_15_fr_en_order6_index0-2000_skip0.csv` (2,728 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order6_index0_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order6_index1000_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order5_index2000_clean_IG.csv` (933 rows)

Results of the collection:

* start time: 2023-03-23 13:57:38
* finish time: 2023-03-24 11:03:18
* errors: 18
  - 7 timeout
  - 0.26% queries timed-out
* results:
  - 1,807,609 tweets collected
  - 2,122 (??%) returned results
  - <span dir="">\~</span>852 tweets per query

Performance of the collection

* duration: 21:05:40
* ratio: 24 tweets / second


### Collection 4 (FINISHED) : Order 7-9, all

Parameters of the collection:

* profile: Kelly
* screen: 342234.pts-0.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march23-collection/Order7-8-9_JPKey_output`
* key: Jean-Philippe
* files
  - `tweet_search_title_2023_03_15_fr_en_order7-order8-order9_skip0.csv` (1,408 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order7_index0_clean_IG.csv` (1,000 rows)
    * `tweet_search_title_2023_03_15_fr_en_order7_index1000_clean_IG.csv` (266 rows)
    * `tweet_search_title_2023_03_15_fr_en_order8_index0_clean_IG.csv` (139 rows)
    * `tweet_search_title_2023_03_15_fr_en_order9_index0_clean_IG.csv` (62 rows)


Results of the collection:

* start time: 2023-03-23 13:59:23
* finish time: 2023-03-23 23:50:32
* errors: 19
  - 3 timeout
  - 0.26% queries timed-out
* results:
  - 911,577 tweets collected
  - 1,140 (81%) returned results
  - <span dir="">\~</span>800 tweets per query

Performance of the collection

* duration: 9:51:0
* ratio: 26 tweets / second

### Collection 5 (FINISHED) : Order 10-12, all

Parameters of the collection:

* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march23-collection/Order10-11-12_BenjaminKey_output`
* key: Benjamin
* files
  - `tweet_search_title_2023_03_15_fr_en_order10-11-12_skip0.csv` (582 rows with skips removed)
  - concatenation of:
    * `tweet_search_title_2023_03_15_fr_en_order10_index0_clean_IG.csv` (113 rows)
    * `tweet_search_title_2023_03_15_fr_en_order11_index0_clean_IG.csv` (479 rows)
    * `tweet_search_title_2023_03_15_fr_en_order12_clean_IG.csv` (25 rows)

Results of the collection:

* start time: 2023-03-23 18:23:43
* finish time: 2023-03-23 21:35:33
* errors: 25
  - 0 timeout
  - 0% queries timed-out
* results:
  - 237,133 tweets collected
  - 481 (82.6%) returned results
  - 493 tweets per query

Performance of the collection

* duration: 3:11:50
* ratio: 21 tweets / second


## March 24 collections

### Collection (FINISHED) 1 : Skipped part 1, where skip is 0

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `march23-skip-unskip/skipped_pt1_skip0_Benjamin_output`
* key: Benjamin
* files
  - `tweet_search_title_2023_03_15_fr_en_skipped_pt1_skip0.csv` (199 rows)

Results of the collection:

* start time: 2023-03-24 08:11:39
* finish time: 2023-03-24 10:44:14
* errors: 2
  - 1 timeout
  - 0.5% queries timed-out
* results:
  - 239,495 tweets collected
  - 171 (86%) returned results
  - <span dir="">\~</span>1,401 tweets per query

Performance of the collection

* duration: 2:32:35
* ratio: 26 tweets / second

### Collection (FINISHED) 2 : Timed-out title queries (30 rows)

Parameters of the collection:

* profile: Kelly
* screen: 365340.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `march24-collection/timeouts_JPKey_output`
* key: Jean-Philippe
* files
  - `last_tweets_collected_for_url_id_all.csv` (30 rows)

Results of the collection:

* start time: 2023-03-24 10:24:35
* finish time: 2023-03-24 16:41:44
* errors: 15
  - 15 timeout
  - 50% queries timed-out
* results:
  - 615,080 tweets collected
  - 30 (100%) returned results
  - <span dir="">\~</span>20,503 tweets per query

Performance of the collection

* duration: 6:17:09
* ratio: 27 tweets / second


### Collection (FINISHED) 3 : Skipped, `docs_movies` Part 1

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `march23-skip-unskip/skipped_pt1_docs_movies_skip0_1-65_Pedro_output`
* key: Pedro
* files
  - `tweet_search_title_2023_03_15_fr_en_skipped_pt1_docs_movies_clean_RR_skip0_1-65.csv` (65 rows)

Results of the collection:

* start time: 2023-03-24 12:11:57
* finish time: 2023-03-24 17:49:17
* errors: 8
  - 7 timeout
  - 10.8% queries timed-out
* results:
  - 521,573 tweets collected
  - 61 (93.8%) returned results
  - <span dir="">\~</span>8,550 tweets per query

Performance of the collection

* duration: 5:37:20
* ratio: 26 tweets / second


### Collection (FINISHED) 4 : Skipped, `docs_movies` Part 2

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `march23-skip-unskip/skipped_pt1_docs_movies_skip0_66-67_Beatrice_output`
* key: Béatrice
* files
  - `tweet_search_title_2023_03_15_fr_en_skipped_pt1_docs_movies_clean_RR_skip0_66-67.csv` (2 rows)

Results of the collection:

* start time: 2023-03-24 19:48:56
* finish time: 2023-03-24 19:49:09
* errors: 0
  - 0 timeout
  - 0% queries timed-out
* results:
  - 271 tweets collected
  - 2 (100%) returned results
  - <span dir="">\~</span>136 tweets per query

Performance of the collection

* duration: 0:00:13
* ratio: 21 tweets / second


### Collection (FINISHED) 5 : Skipped, Part 2

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `march23-skip-unskip/skipped_pt2_Beatrice_output`
* key: Béatrice
* files
  - `tweet_search_title_2023_03_15_fr_en_skipped_pt2_clean_RR.csv` (39 rows)

Results of the collection:

* start time: 2023-03-24 19:52:35
* finish time: 2023-03-24 20:08:56
* errors: 0
  - 0 timeout
  - 0% queries timed-out
* results:
  - 35,709 tweets collected
  - 37 (94.9%) returned results
  - <span dir="">\~</span>965 tweets per query

Performance of the collection

* duration: 0:16:21
* ratio: 36 tweets / second



## March 25 collections
### Collection (FINISHED) 1 : Timed-out title queries (9 rows)

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `march24-collection-achim/timeouts_JPKey_since_tweet_4075f27b5a05a938c17747190397c2ad_JP_output`
* key: Jean-Philippe
* files
  - `march24-collection-achim/datasets/last_tweets_collected_for_url_id_all_since_4075f27b5a05a938c17747190397c2ad.csv` (9 rows)

Results of the collection:

* start time: 2023-03-25 08:54:48
* finish time: 2023-03-25 11:35:11
* errors: 5
  - 5 timeout
  - 55.5% queries timed-out
* results:
  - 193,085 tweets collected
  - 9 (100%) returned results
  - <span dir="">\~</span>21,454 tweets per query

Performance of the collection

* duration: 2:40:23
* ratio: 20 tweets / second


### Collection (FINISHED) 2 : Timed-out title queries (25 rows)

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `march24-collection-achim/timeouts_JPKey_since_tweet_655b843af9f415ce3e0220d661fff798_JP_output`
* key: Jean-Philippe
* files
  - `march24-collection-achim/datasets/last_tweets_collected_for_url_id_all_since_655b843af9f415ce3e0220d661fff798.csv` (25 rows)

Results of the collection:

* start time: 2023-03-25 11:45:51
* finish time: 2023-03-25 16:40:17
* errors: 7
  - 7 timeout
  - 28% queries timed-out
* results:
  - 348,626 tweets collected
  - 25 (100%) returned results
  - <span dir="">\~</span>13,945 tweets per query

Performance of the collection

* duration: 4:54:26
* ratio: 20 tweets / second


### Collection (FINISHED) 3 : Timed-out title queries (? rows)

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `march24-collection-achim/timeouts_JPKey_since_tweet_a41bad7a356dad47c9f728bb26b40541_JP_output`
* key: Jean-Philippe
* files
  - `march24-collection-achim/datasets/last_tweets_collected_for_url_id_all_since_a41bad7a356dad47c9f728bb26b40541.csv` (??? rows) --mal-formatted CSV file

Results of the collection:

* start time: 2023-03-25 16:49:35
* finish time: 2023-03-25 21:50:47
* errors: 12
  - 11 timeout
  - ??? (mal-formatted CSV file) queries timed-out
* results:
  - 486,081 tweets collected
  - 26 returned results
  - <span dir="">\~</span>18,695 tweets per query

Performance of the collection

* duration: 5:01:12
* ratio: 27 tweets / second


## 3 April collections

### Collection 1 (FINISHED) : Titles from duplicated URLs in Condor dataset, EN-FR

Parameters of the collection:

* profile: Kelly
* screen: 2487597.pts-0.gazouilloire2022
* Python environment: `minet3.11`
* directory: `april3-collection/titles_from_duplicate_urls_in_condor_output`
* key: Jean-Philippe
* files
  - `april3-collection/datasets/unique_titles_from_duplicate_urls_in_condor_skip0.csv` (446 rows)

Results of the collection:

* start time: 2023-04-03 14:23:13
* finish time: 2023-04-03 18:45:25
* errors: 4
  - 1 timeout
  - 0.9% queries timed-out
* results:
  - 394,871 tweets collected
  - 267 queries returned results
  - <span dir="">\~</span>1,479 tweets per query

Performance of the collection

* duration: 4:22:12
* ratio: 25 tweets / second


## 8 April collections

### Collection 1 (FINISHED) : Order 1, non-en-fr

Parameters of the collection:

* profile: Kelly
* screen: 2487597.pts-0.gazouilloire2022
* Python environment: `minet3.11`
* directory: `april8-collection/Order1_non_en_fr_titles_BenjaminKey_output`
* key: Benjamin (4.8 million remaining)
* files
  - `spsm_non_EN_FR_condor_true_false_sf_all_order1_unique_titles_skip0.csv` (5,809 rows)

Results of the collection:

* start time: 2023-04-08 09:13:36
* finish time: 2023-04-09 12:04:22
* errors: 20
  - 4 timeout
  - 0.07% queries timed-out
* results:
  - 2,388,340 tweets collected
  - 5,277 queries ( 90.8% ) returned results
  - <span dir="">\~</span>452 tweets per query

Performance of the collection

* duration: 1 day, 2:50:46
* ratio: 25 tweets / second

### Collection 2 (FINISHED) : Order 2, non-en-fr

Parameters of the collection:

* profile: Kelly
* screen: 1000099.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `april8-collection/Order2_non_en_fr_titles_JPKey_output`
* key: Jean-Philippe (6.7 million remaining)
* files
  - `spsm_non_EN_FR_condor_true_false_sf_all_order2_unique_titles_skip0.csv` (1,274 rows)

Results of the collection:

* start time: 2023-04-08 09:16:18
* finish time: 2023-04-08 12:04:47
* errors: 7
  - 0 timeout
  - 0% queries timed-out
* results:
  - 192,843 tweets collected
  - 1,147 queries ( 90% ) returned results
  - <span dir="">\~</span>168 tweets per query

Performance of the collection

* duration: 2:48:29
* ratio: 19 tweets / second


## 9 April collection

### Collection 1 (FINISHED) : Order 3, non-en-fr

Parameters of the collection:

* profile: Kelly
* screen: 1000099.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `april8-collection/Order3_non_en_fr_titles_JPKey_output`
* key: Jean-Philippe
* files
  - `spsm_non_EN_FR_condor_true_false_sf_all_order3_unique_titles_skip0.csv` (4,061 rows)

Results of the collection:

* start time: 2023-04-09 10:02:08
* finish time: 2023-04-09 14:38:56
* errors: 4
  - 1 timeout
  - 0.02% queries timed-out
* results:
  - 182,206 tweets collected
  - 3,134 queries ( 77.1% ) returned results
  - <span dir="">\~</span>58 tweets per query

Performance of the collection

* duration: 4:36:48
* ratio: 11 tweets / second


## 13 April collection

### Collection 1 (FINISHED) : Order 4, non-en-fr

Parameters of the collection:

* profile: Kelly
* screen: 2487597.pts-0.gazouilloire2022 
* Python environment: `minet3.11`
* directory: `april13-collection/Order4_non_en_fr_titles_JPKey_output`
* key: Jean-Philippe
* files
  - `spsm_non_EN_FR_condor_true_false_sf_all_order4_titles_skip0.csv` (2,109 rows)

Results of the collection:

* start time: 2023-04-13 15:02:16
* finish time: 2023-04-13 19:52:56
* errors: 4
  - 1 timeout
  - 0.08% queries timed-out
* results:
  - 313284 tweets collected
  - 1252 queries ( 59.36% ) returned results
  - <span dir="">\~</span>250 tweets per query

Performance of the collection

* duration: 4:50:40
* ratio: 18 tweets / second

### Collection 2 (FINISHED) : Titles from duplicated URLs in Condor dataset, not EN-FR

Parameters of the collection:

* profile: Kelly
* screen: ---
* Python environment: `minet3.11`
* directory: `april13-collection/titles_from_duplicate_urls_in_condor_not_EN-FR_BenjaminKey_output`
* key: Benjamin
* files
  - `unique_titles_from_duplicate_urls_in_condor_skip0_non_EN_FR.csv` (332 rows)

Results of the collection:

* start time: 2023-04-13 15:18:45
* finish time: 2023-04-13 16:39:26
* errors: 0
  - 0 timeout
  - 0.0% queries timed-out
* results:
  - 115731 tweets collected
  - 137 queries ( 41.27% ) returned results
  - <span dir="">\~</span>845 tweets per query

Performance of the collection

* duration: 1:20:41
* ratio: 24 tweets / second


## 15 April collections

### Collection 1 (FINISHED) : Order 5, non-en-fr, index 1-2000, part 1

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april15/order5_1_2000_till_baf229cc9777956d2dc5b4ae321bd1e3_JP_output`
* key: Jean-Philippe
* files
  - `spsm_non_EN_FR_condor_new_rating_5_1_2000_IG_clean_title_skip_0_till_baf229cc9777956d2dc5b4ae321bd1e3.csv` (1,114 rows)

Results of the collection:

* start time: 2023-04-15 15:18:32
* finish time: 2023-04-15 20:03:35
* errors: 2
  - 1 timeout
  - 0.11% queries timed-out
* results:
  - 382,716 tweets collected
  - 933 queries ( 83.75% ) returned results
  - <span dir="">\~</span>410 tweets per query

Performance of the collection

* duration: 4:45:03
* ratio: 22 tweets / second


### Collection 2 (FINISHED) : Order 5, non-en-fr, index 2001-4000

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april15/order5_2001_4000_BT_output`
* key: Benjamin
* files
  - `spsm_non_EN_FR_condor_new_rating_5_2001_4000_RR_clean_title_skip_0.csv` (1,834 rows)

Results of the collection:

* start time: 2023-04-15 15:21:02
* finish time: 2023-04-15 22:54:01
* errors: 5
  - 2 timeout
  - 0.13% queries timed-out
* results:
  - 628,667 tweets collected
  - 1,507 queries ( 82.17% ) returned results
  - <span dir="">\~</span>417 tweets per query

Performance of the collection

* duration: 7:32:59
* ratio: 23 tweets / second

### Collection 3 (FINISHED) : Order 5, non-en-fr, index 4001-6000

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april15/order5_4001_6000_BM_output`
* key: Béatrice
* files
  - `spsm_non_EN_FR_condor_new_rating_5_4001_6651_IG_RR_clean_title_skip_0.csv` (2,441 rows)

Results of the collection:

* start time: 2023-04-15 15:25:56
* finish time: 2023-04-16 00:01:23
* errors: 8
  - 2 timeout
  - 0.1% queries timed-out
* results:
  - 713978 tweets collected
  - 1996 queries ( 81.77% ) returned results
  - <span dir="">\~</span>358 tweets per query

Performance of the collection

* duration: 8:35:27
* ratio: 23 tweets / second

## 16 April collections

### Collection 1 (FINISHED) : Order 5, non-en-fr, index 1-2000, part 2

Parameters of the collection:

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april15/order5_1_2000_baf229cc9777956d2dc5b4ae321bd1e3_onwards_p_output`
* key: Pedro
* files
  - `spsm_non_EN_FR_condor_new_rating_5_1_2000_IG_clean_title_skip_0_baf229cc9777956d2dc5b4ae321bd1e3_onwards.csv` (239 rows)

Results of the collection:

* start time: 2023-04-16 11:55:30
* finish time: 2023-04-16 12:36:25
* errors: 1
  - 1 timeout
  - 0.55% queries timed-out
* results:
  - 44166 tweets collected
  - 181 queries ( 75.73% ) returned results
  - <span dir="">\~</span>244 tweets per query

Performance of the collection

* duration: 0:40:55
* ratio: 18 tweets / second


## 21 April collections

### Collection 1 (FINISHED) : YouTube video titles

Parameters of the collection:

* profile: Kelly
* screen: `1000099.pts-3.gazouilloire2022`
* Python environment: `minet3.11`
* directory: `april21-collection/youtube_video_titles_BeatriceKey_output`
* key: Béatrice
* files:
  - `missing_youtube_title_RR_clean_skip0.csv` (367 rows)

Results of the collection:

* start time: 2023-04-21 09:05:21
* finish time: 2023-04-21 14:06:29
* errors: 5
  - 5 timeout
  - 1.76% queries timed-out
* results:
  - 446323 tweets collected
  - 284 queries ( 77.38% ) returned results
  - <span dir="">\~</span>1572 tweets per query

Performance of the collection

* duration: 5:01:08
* ratio: 25 tweets / second


### Collection 2 (RUN OUT OF CREDITS) : Timed-out queries, never been retried

Parameters of the collection:

* profile: Kelly
* screen: `1000099.pts-3.gazouilloire2022`
* Python environment: `minet3.11`
* directory: `april21-collection/timed-out_as_of_20_april_and_never_retried_BenKey_output`
* key: Benjamin
* files:
  - `timed-out_as_of_20_april_and_never_retried.csv` (23 rows)

Results of the collection:

* start time: 2023-04-21 17:04:14
* finish time: 2023-04-21 19:30:52
* errors: 5
  - 5 timeout
  - 41.67% queries timed-out
* results:
  - 176353 tweets collected
  - _12 queries ( 52.17% ) returned results_ *
  - <span dir="">\~</span>14696 tweets per query

\* _100% (11) returned results before key ran out of credits_

Performance of the collection

* duration: 2:26:38
* ratio: 20 tweets / second



### Collection 3 (FINISHED) : Completed titles from Web Archive

Parameters of the collection:

* profile: Kelly
* screen: `377456.pts-3.gazouilloire2022`
* Python environment: `minet3.11`
* directory: `april21-collection/completed_webarchive_title_BeatriceKey_output`
* key: Béatrice
* files:
  - `completed_empty_title_webarchive_skip0.csv` (1,893 rows)

Results of the collection:

* start time: 2023-04-21 14:41:37
* finish time: 2023-04-22 07:33:56
* errors: 12
  - 5 timeout
  - 0.36% queries timed-out
* results:
  - 1403242 tweets collected
  - 1402 queries ( 74.06% ) returned results
  - <span dir="">\~</span>1001 tweets per query

Performance of the collection

* duration: 16:52:19
* ratio: 23 tweets / second


## 22 April collections

### Collection 1 (FINISHED) : Remainder of timed-out queries, never been retried

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april22-collection/timed-out_as_of_20_april_and_never_retried_from_incl_1f1f95d78f5a96534f4938194ccb011b_Beatrice`
* key: Béatrice
* files:
  - `timed-out_as_of_20_april_and_never_retried_from_incl_1f1f95d78f5a96534f4938194ccb011b.csv` (11 rows)

Results of the collection:

* start time: 2023-04-22 15:09:03
* finish time: 2023-04-22 17:25:55
* errors: 5
  - 5 timeout
  - 50.0% queries timed-out
* results:
  - 250,805 tweets collected
  - 10 queries ( 90.91% ) returned results
  - <span dir="">\~</span>25,080 tweets per query

Performance of the collection

* duration: 2:16:52
* ratio: 31 tweets / second


### Collection 2 (CRASHED) : 1 Timed-out query that was retried but still timed-out

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april22-collection/timed-out_as_of_20_april_and_retried_but_still_timed-out-only-8b9cf22e34b897907c1a1353f5b63a57_Beatrice`
* key: Béatrice
* files:
  - `timed-out_as_of_20_april_and_retried_but_still_timed-out-only-8b9cf22e34b897907c1a1353f5b63a57.csv` (1 row)

Results of the collection:

* start time: 2023-04-22 17:39:42
* finish time: 2023-04-22 18:01:27
* errors: 1
  - 0 timeout*
  - 0% queries timed-out
* results:
  - 712 tweets collected
  - 1 queries ( 100% ) returned results
  - <span dir="">\~</span>712 tweets per query

\* One query did time out, but there was some sort of problem with the API and that query did not return any results. The only query to return results did not time out.

Performance of the collection

* duration: 0:21:45
* ratio: 1 tweets / second


### Collection 3 (FINISHED) : Remaining timed-out queries that were retried but still timed out

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april22-collection/timed-out_as_of_20_april_and_retried_but_still_timed-out-from-incl-Benjamin_output`
* key: Benjamin
* files:
  - `timed-out_as_of_20_april_and_retried_but_still_timed-out-from-incl-` (12 rows) (CSV file is missing file extension)

Results of the collection:

* start time: 2023-04-24 18:39:28
* finish time: 2023-04-24 21:32:07
* errors: 6
  - 6 timeout
  - 54.55% queries timed-out
* results:
  - 258883 tweets collected
  - 11 queries ( 91.67% ) returned results
  - <span dir="">\~</span>23535 tweets per query

Performance of the collection

* duration: 2:52:39
* ratio: 25 tweets / second


### Collection 4 (FINISHED) : Order 1 of not eligible from non EN/FR

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april22-collection/spsm_non_EN_FR_not_eligible_order1_IG_RR_unique_titles_skip_0_v2_Beatrice_output`
* key: Béatrice
* files:
  - `spsm_non_EN_FR_not_eligible_order1_IG_RR_unique_titles_skip_0_v2.csv` (661 rows) 

Results of the collection:

* start time: 2023-04-24 17:08:46
* finish time: 2023-04-24 20:13:34
* errors: 4
  - 1 timeout
  - 0.19% queries timed-out
* results:
  - 290182 tweets collected
  - 518 queries ( 78.37% ) returned results
  - <span dir="">\~</span>560 tweets per query

Performance of the collection

* duration: 3:04:48
* ratio: 26 tweets / second


### Collection 5 (FINISHED) : Order 2 of not eligible from non EN/FR

* profile: Achim
* screen: ---
* Python environment: ---
* directory: `april22-collection/spsm_non_EN_FR_not_eligible_order2_unique_titles_skip0_Benjamin_output`
* key: Benjamin
* files:
  - `spsm_non_EN_FR_not_eligible_order2_unique_titles_skip0.csv` (331 rows)

Results of the collection:

* start time: 2023-04-24 23:57:11
* finish time: 2023-04-25 01:41:43
* errors: 220
  - 0 timeout
  - 0.0% queries timed-out
* results:
  - 24688 tweets collected
  - 80 queries ( 24.17% ) returned results
  - <span dir="">\~</span>309 tweets per query

Performance of the collection

* duration: 1:44:32
* ratio: 4 tweets / second


## 27 April collections

### Collection 1 : Re-do timed-out queries

* profile: Kelly
* screen: 377456.pts-3.gazouilloire2022
* Python environment: `minet3.11`
* directory: `april27-collection/title_timeouts_as_of_25_april_BeatriceKey_output`
* key: Béatrice
* files:
  - `title_timeouts_as_of_25_april.csv` (11 rows) # poorly named, were processed on 26 April

Results of the collection:

* start time: 2023-04-27 15:41:38
* finish time: 2023-04-27 19:03:37
* errors: 1
  - 1 timeout
  - 9.09% queries timed-out
* results:
  - 1219973 tweets collected
  - 11 queries ( 100.0% ) returned results
  - <span dir="">\~</span>110907 tweets per query

Performance of the collection

* duration: 3:21:59
* ratio: 101 tweets / second