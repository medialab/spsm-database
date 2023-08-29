# Language detection on text scraped from web page's HTML

## Set up

- Create/activate virtual environment: Python version 3.11.4
- Install Python dependencies: `pip install -r requirements.txt`
- Install SpaCy language package: `python -m spacy download en_core_web_sm`

## Usage

Run `main.py` script on the CSV file of de-duplicated claim URLs that has the scraped HTML. The file is too large to store on any private GitHub repo, but it is stored on Sciences Po's private GitLab, in the SPSM group's projetct "SPSM General" ([`./data/fixed_sources_table.csv.gz`](https://gitlab.sciences-po.fr/spsm/spsm/-/blob/main/data/fixed_sources_table.csv.gz)).

```shell
python main.py --infile URLS_WITH_HTML_TEXT --outfile URLS_WITH_LANG_AND_TEXT
```

The script reads a very large file and outputs a very large file. The out-file retains the scraped HTML text because it is useful, along with the detected language, for NLP analysis and annotations that will be associated with URLs in the database.

## Credits

The language detection is performed by [`spacy_fastlang`](https://github.com/thomasthiebaud/spacy-fastlang).

> Thomas Thiebaud. (2023, July 30). spacy-fastlang: Language detection using Spacy and Fasttext. GitHub. https://github.com/thomasthiebaud/spacy-fastlang

The web page text was scraped using [`minet`](https://github.com/medialab/minet).

> Guillaume Plique, Pauline Breteau, Jules Farjas, Héloïse Théro, Jean Descamps, Amélie Pellé, & Laura Miguel. (2019, October 14). Minet, a webmining CLI tool & library for python. Zenodo. http://doi.org/10.5281/zenodo.4564399
