import casanova
import re
import click
import sys
import csv

csv.field_size_limit(sys.maxsize)

booleans = ['and', 'or']

def clean_word(word):
    if word not in booleans:
        try:
            int(word)
        except:
            if len(word) > 1:
                return word
        else:
            return word


@click.command()
@click.argument('infile')
@click.argument('outfile')
def main(infile, outfile):
    with open(infile) as f, open(outfile, 'w') as of:
        additional_headers = ['query_url', 'query_title']
        enricher = casanova.enricher(f, of, add=additional_headers)
        title_pos = enricher.headers['condor_share_title']
        web_title_pos = enricher.headers['webpage_title']
        for row, url in enricher.cells('normalized_url', with_rows=True):

            # Clean URL
            query_url = url
            if len(url) > 126:
                shortened_url = url[:126]
                url_pieces = shortened_url.split('-')
                query_url = "-".join(url_pieces[:-1])

            # Clean title
            if not row[title_pos]:
                query_title = row[web_title_pos]
            else:
                query_title = row[title_pos]

            if 'https://www.' in query_title or 'http://www.' in query_title:
                query_title = ''

            query_title = re.sub(r'\s*[^A-Za-zÀ-Öß-ÿ0-9]\s*', ' ', query_title)
            query_title = query_title.lower()
            title_pieces = query_title.split()
            query_title = " ".join([word for word in title_pieces if clean_word(word)])
            if len(query_title.split()) < 3:
                query_title = ''
            if len(query_title) > 126:
                shortened_title = query_title[:126]
                title_pieces = shortened_title.split()
                query_title = " ".join(title_pieces[:-1])
            enricher.writerow(row, [query_url, query_title])


if __name__ == "__main__":
    main()
