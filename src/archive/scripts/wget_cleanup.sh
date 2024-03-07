#!/bin/bash

ARCHIVE_DIR=$1
LOG_FILE=../../$2
PATHS_FILE=../../$3

cd $ARCHIVE_DIR
cat $LOG_FILE | grep -E "Sauvegarde|Saving" > $PATHS_FILE
cd -