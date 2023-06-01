import casanova
import re
import click
import sys
import csv
from hashlib import md5

csv.field_size_limit(sys.maxsize)

booleans = ['and', 'or']


@click.command()
@click.argument('infile')
@click.argument('outfile')
def main(infile, outfile):
    with open(infile) as f, open(outfile, 'w') as of:
        additional_headers = ['complete_query_title_id','complete_query_title']
        enricher = casanova.enricher(f, of, add=additional_headers)
        title_pos = enricher.headers['condor_share_title']
        web_title_pos = enricher.headers['webpage_title']
        domain_pos = enricher.headers['domain']
        for row in enricher:

            # If present, select the prioritized title
            if not row[title_pos]:
                query_title = row[web_title_pos]
            else:
                query_title = row[title_pos]

            # Ignore titles if they are urls
            if 'https://www.' in query_title or 'http://www.' in query_title:
                query_title = ''

            # Cast the title in lowercase letters and tokenize it
            query_title = query_title.lower()
            title_tokens = query_title.split()

            # If present, remove the domain name from the end of the title
            domain_name = row[domain_pos]
            hostname = None
            if domain_name and len(domain_name.split('.')) > 1:
                hostname = domain_name.split('.')[0]
            if title_tokens and len(title_tokens[-1]) > 1:
                if title_tokens[-1] == domain_name or (hostname and title_tokens[-1] == hostname):
                    title_tokens.pop()
                    query_title = ' '.join(title_tokens)

            # Remove all characters that are:
            # 1. not in the approved alphabets (A-Z,a-z,À-Ö,ß-ÿ)
            # 2. not numbers (0-9)
            # 3. not approved punctuation ('`´‘’“”,.)
            query_title = re.sub(r'\s*[^A-Za-zÀ-Öß-ÿ0-9"\'`´‘’“”,\.]\s*', ' ', query_title)

            # If the query title is too long, cut it off at the last token 
            if len(query_title) > 126:
                shortened_title = query_title[:126]
                title_tokens = shortened_title.split()
                query_title = ' '.join(title_tokens[:-1])
            
            # Enclose boolean operators in double quotation marks
            title_tokens = query_title.split()
            new_title_tokens = []
            for token in title_tokens:
                if token in booleans:
                    token = '"'+token+'"'
                new_title_tokens.append(token)
            query_title = ' '.join(new_title_tokens)

            # Again, adjust title for length
            if len(query_title) > 126:
                shortened_title = query_title[:126]
                title_tokens = shortened_title.split()
                query_title = ' '.join(title_tokens[:-1])

            query_title_id = md5(str.encode(query_title)).hexdigest()
            enricher.writerow(row, [query_title_id, query_title])


if __name__ == "__main__":
    main()
