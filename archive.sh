#!/bin/bash

DATAFILE=$1  # CSV containing columns "url" and "normalized_url_hash"
ARCHIVEDIR=$2  # Directory in which the archive will be created

mkdir -p $ARCHIVEDIR  # Make the directory if it doesn't already exist

xsv select archive_url,url_id $DATAFILE |
  xsv behead |
  while read line; do 
    archive_url=$(echo $line | xsv select 1) # assigne variable for the url
    echo "$archive_url"
    url_id=$(echo $line | xsv select 2) # assigne variable for hash 
    first_char=$(echo $url_id | sed -r 's/^(.).*$/\1/')
    log_dir=log_$first_char
    path_dir=path_$first_char
    mkdir -p $log_dir $path_dir 
    logfile="${url_id}_log"  # assign variable for log file
    #pathsfile="${url_id}_paths"  # assign variable for path file
    # timestamp=$(date +"%F %H:%M:%S") # assign variable for timestamp --> not usefull because already the first line of the logfile

    curl -sL "https://web.archive.org/save/$archive_url" > /dev/null

    cd $ARCHIVEDIR  # go into the archive
      # do everything you need to do
      wget -E -H -k -K -p "$archive_url" -o ../$log_dir/${url_id}_log
      main_pathfile=$(cat ../$log_dir/${url_id}_log | grep "Sauvegarde" | head -1 | tr '«' ',' | tr '»' ' ' | cut -d',' -f2)  
      echo "url: ${archive_url}" # url of the fake news 
      echo "logfile: ${logfile}" # hash 
      echo "path_html: ${main_pathfile}" # path of the saved html
      # echo "timestamp:${timestamp}" # timestamp of the wget command but alreadw in the logfile
      # echo "URL archived at: ${timestamp}" >> logfile #the timestamp is already in the logfile
      cat ../$log_dir/${url_id}_log | grep "Sauvegarde" | tr '«' ',' | tr '»' ' ' | cut -d',' -f2 > ../$path_dir/${url_id}_paths
      echo "path_file: ${url_id}_paths" 
      echo ""

    cd .. # go back to the top-level, where the script is saved / from where the script is deployed
    sleep 4
    done

# INPUT CSV : archive_url,url_id
# in the script : url,logfile,pathsfile,timestamp

# tested and work on the url from de facto !!