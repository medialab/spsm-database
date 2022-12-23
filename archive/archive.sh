#!/bin/bash

DATAFILE=$1  # CSV containing columns "url" and "normalized_url_hash"

xsv select archive_url,url_id $DATAFILE |
  xsv sort -u -s url_id |
  xsv behead |
  while read line; do 
    archive_url=$(echo $line | xsv select 1) # assigne variable for the url
    echo "$archive_url"
    url_id=$(echo $line | xsv select 2) # assigne variable for hash 
    first_char=$(echo $url_id | sed -r 's/^(.).*$/\1/')
    first_three=$(echo $url_id | sed -r 's/^(.{3}).*$/\1/')
    ARCHIVEDIR="${first_char}/${first_three}"
    mkdir -p $ARCHIVEDIR
    log_dir=log_$first_char
    path_dir=path_$first_char
    mkdir -p $log_dir $path_dir 

    curl -sL "https://web.archive.org/save/$archive_url" > /dev/null

    cd $ARCHIVEDIR  # go into the archive

      logfile="../../${log_dir}/${url_id}_log"
      pathsfile="../../${path_dir}/${url_id}_paths"

      # do everything you need to do
      wget -E -H -k -K -p "$archive_url" -o $logfile
      main_pathfile=$(cat $logfile | grep "Sauvegarde" | head -1)  
      echo "url: ${archive_url}" # url of the fake news 
      echo "logfile: ${logfile}" # hash 
      echo "path_html: ${main_pathfile}" # path of the saved html
      cat $logfile | grep "Sauvegarde" > $pathsfile
      echo "path_file: $pathsfile" 
      echo ""

    cd - # go back to the top-level, where the script is saved / from where the script is deployed
    sleep 4
    done

# INPUT CSV : archive_url,url_id
# in the script : url,logfile,pathsfile,timestamp

# tested and work on the url from de facto !!
