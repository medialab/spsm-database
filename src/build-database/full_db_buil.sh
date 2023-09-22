#!/bin/bash

CONFIG=$1
TWEET_FILES=$2

# Import all the finalized data files that constitute claim metadata
python src/ingest.py $CONFIG --data-source condor --no-prompt
python src/ingest.py $CONFIG --data-source "de facto" --no-prompt
python src/ingest.py $CONFIG --data-source "science feedback" --no-prompt
python src/ingest.py $CONFIG --data-source "completed urls" --no-prompt
# python src/ingest.py $CONFIG --data-source "searchable titles and urls" --no-prompt
python src/ingest.py $CONFIG --data-source "supplemental titles" --no-prompt

# Merge the data sources into a claims table and build relations
# python src/merge.py $CONFIG

# # Ingest tweet data into the database
# python src/tweets.py ingest-data --config $CONFIG $TWEET_FILES

# # Build relations between tweets and claims
# python src/tweets.py build-relations --config $CONFIG