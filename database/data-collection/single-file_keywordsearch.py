import subprocess
import click
import datetime
from pathlib import Path
from time import sleep
import csv
import os
import casanova
from tqdm.auto import tqdm
import timeit
from twitwi.constants import TWEET_FIELDS

TWEETSEARCH_BASIC = ['minet', 'twitter', 'tweet-search', '--rcfile']
TWEETSEARCH_ACADEMIC = ['--start-time', '2006-03-21T00:00:00Z', '--academic']


@click.command()
@click.option('--datafile', required=True, help='Path to the CSV data file.')
@click.option('--reverse', is_flag=True, show_default=True, default=False, required=False, help='Flag signaling to process the data file in reverse.')
@click.option('--dir', required=True, help='Name of the directory in which the output will be written. It is advisable to include the name of the key.')
@click.option('--rcfile', required=True, help='Path to the YAML file with the API key credentials.')
@click.option('--query-col', required=True, help='Name of the column that contains the query to send to the API.')
@click.option('--not-academic', is_flag=True, show_default=True, default=False, required=False, help='Flag signalging to *not* use academic options.')
def main(datafile, reverse, dir, rcfile, query_col, not_academic):
    """Main function for querying the Twitter API."""

    # Make the output directory for this data collection
    output_dir = os.path.join('.', f'{dir}_output')
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Create a file path for a log of all the processed IDs
    processed_ids_filepath = os.path.join(output_dir, 'processed_ids.csv')
    if not os.path.isfile(processed_ids_filepath):
        with open(processed_ids_filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['url_id'])

    # Create a file path for a log of all the results 
    results_filepath = os.path.join(output_dir, 'results.csv')
    if not os.path.isfile(results_filepath):
        with open(results_filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['url_id', 'query_duration', 'query']+TWEET_FIELDS)

    # Create a file path for a log of all the errors
    errors_filepath = os.path.join(output_dir, 'errors.csv')
    if not os.path.isfile(errors_filepath):
        with open(errors_filepath, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['url_id', 'query', 'timeout', 'error_message'])

    # If this directory has a list of already processed IDs, read them to a list
    processed_ids = []
    with open(processed_ids_filepath, 'r') as f:
        reader = casanova.reader(f)
        [processed_ids.extend(row) for row in reader]

    # In append mode, open the processed IDs log, the results file, and the errors file for this collection directory
    with open(processed_ids_filepath, 'a') as open_processed_ids_file, open(errors_filepath, 'a') as open_error_file, open(results_filepath, 'a') as open_results_file:

        # Create a writer object for the log of processed IDs
        processed_ids_writer = csv.writer(open_processed_ids_file)

        # Create a writer object for the error log
        errors_writer = csv.writer(open_error_file)

        # Create a writer object for the results
        results_writer = csv.writer(open_results_file)

        # Prepare to read through the incoming data file
        total = casanova.reader.count(datafile)
        with open(datafile) as f:
            if reverse:
                datafile_reader = casanova.reverse_reader(f)
            else:
                datafile_reader = casanova.reader(f)
            id_pos = datafile_reader.headers['url_id']

            # If the query's associated ID is not in the list of already processed IDs,
            # try getting a result from the API for that query
            for row, query in tqdm(datafile_reader.cells(query_col, with_rows=True), total=total, desc=f'Datafile {datafile}'):
                url_id = row[id_pos]
                if url_id not in processed_ids:
                    print(f'--- source no. {url_id}, querying "{query}"')
                    get_results_for_one_query(
                        url_id=url_id,
                        query=query,
                        rcfile=rcfile,
                        output_dir=output_dir,
                        errors_writer=errors_writer,
                        results_writer=results_writer,
                        not_academic=not_academic
                    )

                    # Regardless the success of the API request, log the ID as having been processed
                    processed_ids_writer.writerow([url_id])

                else:
                    print(f'--- source no. {url_id} is already processed')


def get_results_for_one_query(url_id, query, rcfile, output_dir, errors_writer, results_writer, not_academic):
    """Function that performs the actual query to the Twitter API and writes output."""

    # Generate a unique filepath for this query's results
    query_outfile = os.path.join(output_dir, unique_file_name())

    # Concatenate the minet script with the appropriate arguments
    if not_academic:
        script = TWEETSEARCH_BASIC+[rcfile, '-o', query_outfile]+[query]
    else:
        script = TWEETSEARCH_BASIC+[rcfile, '-o', query_outfile]+TWEETSEARCH_ACADEMIC+[query]

    # In a subprocess, use minet CLI to call the Twitter API
    timer = Timer()
    timeout_reached = False
    try:
        completed_process = subprocess.run(script, capture_output=True, timeout=1200)
    except subprocess.TimeoutExpired as e:
        timeout_reached = True
    duration = timer.stop()

    # If the query was unsuccessful, write the ID and the error message to the error log
    if timeout_reached:
        errors_writer.writerow([url_id, True, "QUERY INCOMPLETE AUTOMATICALLY STOPPED AFTER 1200s TIMEOUT REACHED, RESULTS STORED ANYWAYS"])
        # Because a timed-out query returns some results, append them to the results file
        with open(query_outfile) as qf:
            results_reader = casanova.reader(qf)
            for row in results_reader:
                results_writer.writerow([url_id, duration]+row)

    # If the subprocess returned an error that wasn't a timeout, it is assumed that 
    # there were no results from the query. Log the problematic ID and the error message
    elif completed_process.returncode:
        errors_writer.writerow([url_id, query, False, completed_process.stderr.decode()])

    # If the query was successful, read the results that minet generated 
    # and append them to this directory's results file
    else:
        with open(query_outfile) as qf:
            results_reader = casanova.reader(qf)
            for row in results_reader:
                results_writer.writerow([url_id, duration]+row)

    # Clean up and remove the query results file that minet generated
    os.remove(query_outfile)


# ------------------------------------------------------------- # 
# Helper functions / classes
class Timer():
    def __init__(self) -> None:
        self.start = timeit.default_timer()

    def stop(self):
        delta = timeit.default_timer() - self.start
        return str(datetime.timedelta(seconds=round(delta)))


def concatenate_filepath():
    time = datetime.datetime.now().isoformat()
    time = '-'.join(time.split())
    time = ''.join(time.split('.')[:-1])
    return Path('keyword_search_{}.csv'.format(time))


def unique_file_name():
    filepath = concatenate_filepath()
    if filepath.is_file():
        sleep(1)
        filepath = concatenate_filepath()
    return filepath.name
# ------------------------------------------------------------- # 


if __name__ == "__main__":
    main()
