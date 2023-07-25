# 5 April note

Note on [collection #1, Orders 1-2 from beyond EN/FR](twitter-url-collection-running-notes.md/#5-april-collections).

The `keyword` script, rather than the `url` script, was mistakenly used for this collection. The collection was stopped prematurely and restarted on 6 April with the right script. Nevertheless, we have reason to believe the `keyword` script returned satisfactory results.

First, our own tests have asserted that, under the condition the URL does not surpass 126 characters, a general `keyword` search and a keyword search with the `url:` parameter return the same results.

Second, all tweet searches are performed via the Twitter API `tweets/search/` endpoint. When no special parameters are given, the API searches for the given query, also known as an operator, "within the body or urls of a Tweet," including text and hashtags. When the `url:` parameter is given, the API restricts its search to only "urls of a Tweet." The parameter changes where the API searches for a match, but not how it tokenizes the keyword. The second difference is in the character limits afforded to `tweets/search`. Without any parameters, the search has a lower character limit compared to searches with the `url:` parameter.

Theoretically, the general keyword search should return more results than a search with the `url:` parameter because it could, theoretically, find a URL in other attributes of a tweet, such as data defined as text but not a URL. However, Twitter usually does a good job of identifying what is a URL. Therefore, when the given query is a URL, both the general keyword search and the same search with the paramter `url:` return the same resultsl because they are tokenizing the keyword in the same way and matching the tokenized keyword in expanded versions of the URL. Note, the general keyword search matches the tokenized keyword "on both URLs and unwound URLs within a Tweet."

See [Twitter's documentation](https://developer.twitter.com/en/docs/twitter-api/premium/search-api/guides/operators) below:

|**Operator**|**Description**|
|--|--|
|keyword|Matches a tokenized keyword within the body or urls of a Tweet. This is a tokenized match, meaning that your keyword string will be matched against the tokenized text of the Tweet body – tokenization is based on punctuation, symbol, and separator Unicode basic plane characters. For example, a Tweet with the text “I like coca-cola” would be split into the following tokens: I, like, coca, cola. These tokens would then be compared to the keyword string used in your rule. To match strings containing punctuation (for example, coca-cola), symbol, or separator characters, you must use a quoted exact match as described below.|
||**Note**: This operator will match on both URLs and unwound URLs within a Tweet.|

|**Operator**|**Description**|
|--|--|
|url:|Performs a tokenized (keyword/phrase) match on the expanded URLs of a tweet (similar to url_contains). Tokens and phrases containing punctuation or special characters should be double-quoted. For example, url:"/developer". While generally not recommended, if you want to match on a specific protocol, enclose in double-quotes: url:"https://developer.twitter.com".|
||**Note**: When using PowerTrack or Historical PowerTrack, this operator will match on URLs contained within the original Tweet of a Quote Tweet. For example, if your rule includes url:"developer.twitter.com", and a Tweet contains that URL, any Quote Tweets of that Tweet will be included in the results. This is not the case when using the Search API.

Given (a) the mechanics of how Twitter's `tweet/search/` API endpoint tokenizes and matches keywords, and (b) our own tests of the endpoint with and without the `url:` parameter, we can interpret the results of the 5 April collection in the same way we interpert results fo other collections with the `url:` parameter added to the `tweet/search` query.
