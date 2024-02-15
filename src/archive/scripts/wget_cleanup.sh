#!/bin/bash

ARCHIVE_DIR=$1
LOG_FILE=../../$3
PATHS_FILE=../../$4

cd $ARCHIVE_DIR
cat $LOG_FILE | grep -E "Sauvegarde|Saving" > $PATHS_FILE
cd -