#!/bin/bash

ARCHIVE_DIR=$1
ARCHIVE_URL=$2
LOG_FILE=../../$3
PATHS_FILE=../../$4

cd $ARCHIVE_DIR
wget -E -H -k -K -p --ignore-tags=source,audio --timeout=120 --tries=10 --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3" "$ARCHIVE_URL" -o $LOG_FILE
cat $LOG_FILE | grep -E "Sauvegarde|Saving" > $PATHS_FILE
cd -
