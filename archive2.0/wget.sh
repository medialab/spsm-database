#!/bin/bash

ARCHIVE_DIR=$1
ARCHIVE_URL=$2
LOG_FILE=../../$3
PATHS_FILE=../../$4

cd $ARCHIVE_DIR
wget -E -H -k -K -p --progress=bar:force --show-progress --ignore-tags=source --timeout=120 --tries=10 "$ARCHIVE_URL" -o $LOG_FILE
cat $LOG_FILE | grep -E "Sauvegarde|Saving" > $PATHS_FILE
cd -
