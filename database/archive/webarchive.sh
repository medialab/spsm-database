#!/bin/bash

ARCHIVE_URL=$1

curl -sL "https://web.archive.org/save/$ARCHIVE_URL" > /dev/null
