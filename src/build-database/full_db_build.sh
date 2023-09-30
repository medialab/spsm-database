#!/bin/bash

CONFIG=$1

# Import all the finalized data files that constitute claim metadata
python src/ingest.py $CONFIG --data-source condor --no-prompt
python src/ingest.py $CONFIG --data-source "de facto" --no-prompt
python src/ingest.py $CONFIG --data-source "science feedback" --no-prompt
python src/ingest.py $CONFIG --data-source "completed urls" --no-prompt
python src/ingest.py $CONFIG --data-source "supplemental titles" --no-prompt
python src/ingest.py $CONFIG --data-source "query titles" --no-prompt
python src/ingest.py $CONFIG --data-source "query urls" --no-prompt

# Merge the data sources into a claims table and build relations
python src/run_sql.py --config $CONFIG src/sql/make_claims_table.sql
python src/run_sql.py --config $CONFIG src/sql/make_claims_title_relations.sql

# Make relations between claims and tweets
python src/run_sql.py --config $CONFIG src/sql/make_tweet_claim_relations.sql
