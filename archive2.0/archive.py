import subprocess
import click
import os
import re
import casanova
from datetime import datetime
import time


class WgetParams:
    def __init__(self, full_hash):
        self.archive_parent_dir = f"{full_hash[0]}_archive"
        self.archive_dir = os.path.join(self.archive_parent_dir, full_hash[:3])
        self.log_dir = f"{full_hash[0]}_log"
        self.path_dir = f"{full_hash[0]}_path"
        self.log_file = os.path.join(self.log_dir, f"{full_hash}_log")
        self.paths_file = os.path.join(self.path_dir, f"{full_hash}_paths")


@click.command
@click.argument("infile")
@click.argument("outfile")
def main(infile, outfile):

    # Test the path to the in-file
    if not os.path.isfile(infile): raise FileNotFoundError

    # Set and test paths for the bash scripts
    CURL_SCRIPT = os.path.join(".","webarchive.sh")
    WGET_SCRIPT = os.path.join(".","wget.sh")
    if not os.path.isfile(CURL_SCRIPT): raise FileNotFoundError
    if not os.path.isfile(WGET_SCRIPT): raise FileNotFoundError

    # Regex of last line in the log of a failed Wget
    fail = re.compile(r"dans 0 fichiers|in 0 files")

    # With casanova, build an enricher using the in- and out-files
    with open(infile, "r") as f, \
        open(outfile, 'w') as of:
        enricher = casanova.enricher(f, of)

        # Outside the loop, get the positions of the in-file's headers
        url_id_pos = enricher.headers.url_id
        archive_url_pos = enricher.headers.archive_url
        archive_timestamp_po = enricher.headers.archive_timestamp

        # Inside the loop, parse the values of relevant cells
        for row in enricher:
            hash = row[url_id_pos]
            url = row[archive_url_pos]
            # Set file and folder paths according to hash
            wget = WgetParams(full_hash=hash)

            print(f"\nWorking on '{url}'")

            # If the row has not already been archived with Wget
            if not (os.path.exists(wget.log_file) and os.path.getsize(wget.log_file)):
                # Make the necessary folder structure
                if not os.path.isdir(wget.archive_parent_dir): os.mkdir(wget.archive_parent_dir)
                if not os.path.isdir(wget.archive_dir): os.mkdir(wget.archive_dir)
                if not os.path.isdir(wget.log_dir): os.mkdir(wget.log_dir)
                if not os.path.isdir(wget.path_dir): os.mkdir(wget.path_dir)

                # Call the bash subprocess for Wget
                archive_time = datetime.utcnow()
                print(f"\nCalling Wget ON URL")
                subprocess.run([
                    WGET_SCRIPT, # command
                    wget.archive_dir, # $1
                    url, # $2
                    wget.log_file, # $3
                    wget.paths_file, # $4
                ])

                # Call the bash subprocess for web.archive.org
                print(f"Sending URL to Web Archive")
                subprocess.run([
                    CURL_SCRIPT, # command
                    url, # $1
                ])

                # Give some breath
                time.sleep(5)

            archive_time = os.path.getmtime(wget.log_file)
            row[archive_timestamp_po] = archive_time

            # Regardless of Wget success, write row to out-file
            enricher.writerow(row)


if __name__ == "__main__":
    main()
