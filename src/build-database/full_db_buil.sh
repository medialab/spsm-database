#!/bin/bash

CONFIG=$1
TWEET_FILES=$2

python ingest.py $CONFIG --data-source condor --no-prompt

python ingest.py $CONFIG --data-source "de facto" --no-prompt

python ingest.py $CONFIG --data-source "science feedback" --no-prompt

python ingest.py $CONFIG --data-source "completed urls" --no-prompt

python ingest.py $CONFIG --data-source "searchable titles and urls" --no-prompt

python merge.py $CONFIG

python tweets.py import --config $CONFIG $TWEET_FILES

python tweets.py relation --config $CONFIG