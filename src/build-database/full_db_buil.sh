#!/bin/bash

CONFIG=$1

python ingest.py $CONFIG --data-source condor --no-prompt

python ingest.py $CONFIG --data-source "de facto" --no-prompt

python ingest.py $CONFIG --data-source "science feedback" --no-prompt

python ingest.py $CONFIG --data-source "completed urls" --no-prompt

python ingest.py $CONFIG --data-source "searchable titles and urls" --no-prompt

python merge.py $CONFIG