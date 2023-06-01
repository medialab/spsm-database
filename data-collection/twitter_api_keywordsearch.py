import csv
import os
from hashlib import md5

import casanova
import click
import yaml
from twitwi import (TwitterWrapper, format_tweet_as_csv_row,
                    normalize_tweets_payload_v2)
from twitwi.constants import TWEET_FIELDS
from yaml.loader import SafeLoader


@click.command()
@click.option('--datafile', required=True, help='Path to the CSV data file.')
@click.option('--dir', required=True, help='Name of the directory in which the output will be written. It is advisable to include the name of the key.')
@click.option('--rcfile', required=True, help='Path to the YAML file with the API key credentials.')
@click.option('--query-col', required=True, help='Name of the column that contains the query to send to the API.')
@click.option('--query-id-col', required=False, help='Name of the column that contains the query ID.')
@click.option('--not-academic', is_flag=True, show_default=True, default=False, required=False, help='Flag signalging to *not* use academic options.')
def main(datafile, dir, rcfile, query_col, query_id_col, not_academic):

    # Get API credentials from config file
    with open(rcfile) as f:
        config = yaml.load(f, Loader=SafeLoader)['twitter']

    # Set up files for output
    out_dir = f'{dir}_output'
    os.makedirs(out_dir, exist_ok=True)
    log_filepath = set_up_outfile(
        directory=out_dir,
        filename='log.csv',
                                        # Need to add timeout column
        headers=['query_id', 'query', 'nb_results', 'error_message']
    )
    processed_ids_filepath = set_up_outfile(
        directory=out_dir,
        filename='processed_ids.csv',
        headers=['query_id']
    )
    results_filepath = set_up_outfile(
        directory=out_dir,
        filename='results.csv',
        headers=['query_id', 'query', TWEET_FIELDS]
    )

    # Instantiate the Twitter API wrapper with the credentials
    wrapper = TwitterWrapper(
        config["access_token"],
        config["access_token_secret"],
        config["api_key"],
        config["api_secret_key"],
        listener=None,
        api_version="2"
    )

    # params taken from: https://github.com/python-twitter-tools/twitter/tree/api_v2
    v2_params={
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
        "user.fields":  "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
        "expansions": "author_id,referenced_tweets.id,referenced_tweets.id.author_id,entities.mentions.username,attachments.poll_ids,attachments.media_keys,in_reply_to_user_id,geo.place_id"
        }
    
    # Determine the route based on academic credentials
    route = ["tweets", "search", "all"]
    if not_academic:
        route = ["tweets", "search", "recent"]

    # Open output files to append results
    with open(datafile) as f,\
        open(results_filepath, 'a') as of_results,\
        open(log_filepath, 'a') as of_log,\
        open(processed_ids_filepath, 'a') as of_ids:
        results_writer = csv.writer(of_results)
        log_writer = csv.writer(of_log)
        processed_ids_writer = csv.writer(of_ids)
        datafile_reader = casanova.reader(f)
        query_pos = datafile_reader.headers[query_col]
        if query_id_col:
            query_id_col_pos = datafile_reader.headers[query_id_col]

        # Call the API and write the output
        for row in datafile_reader:
            query = row[query_pos]
            if query_id_col:
                query_id = row[query_id_col_pos]
            else:
                query_id = md5(str.encode(query)).hexdigest()
            nb_tweets = 0
            error = None
            # Need to add timeout on wrapper.call()
            try:
                result = wrapper.call(
                    route=route,
                    query=query,
                    params=v2_params
                )
            except:
                error = result
            else:
                normalized_tweets = normalize_tweets_payload_v2(result, collection_source='api')
                nb_tweets = len(normalized_tweets)
                for tweet in normalized_tweets:
                    results_writer.writerow([query_id, query]+format_tweet_as_csv_row(tweet))
            processed_ids_writer.writerow([query_id])
                                # Need to add timeout to log row
            log_writer.writerow([query_id, query, nb_tweets, error])


def set_up_outfile(directory, filename, headers):
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
    return filepath


if __name__ == "__main__":
    main()