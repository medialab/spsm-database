# Language detection on text scraped from web page's HTML

## Set up

- Create/activate virtual environment: Python version 3.11.4
- Install Python dependencies: `pip install -r requirements.txt`

## Usage

Run `main.py` script on the CSV produced by the `main.py` script in `enrich_database/language_detection/`, which has the column `detected_language` and retains the in-file's column `webpage_text`. For the purposes of summarization, these two data fields are needed.

To run the summarization script, provide the in-file and out-file paths as well as what languages you want to summarize.

```shell
python main.py --infile TEXT_WITH_LANG --outfile SUMMARY -l en -l fr
```

## Credits

The English-language summary is realized by the model [XL-Sum](https://huggingface.co/csebuetnlp/mT5_multilingual_XLSum).

> Tahmid Hasan, Abhik Bhattacharjee, Md. Saiful Islam, Kazi Mubasshir, Yuan-Fang Li, Yong-Bin Kang, M. Sohel Rahman, & Rifat Shahriyar. (2021, August). XL-Sum: Large-Scale Multilingual Abstractive Summarization for 44 Languages. Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021. https://aclanthology.org/2021.findings-acl.413

The French-language summary is realized by the model [camembert2camembert_shared-finetuned-french-summarization](https://huggingface.co/mrm8488/camembert2camembert_shared-finetuned-french-summarization)

> Manuel Romero. (2023, April). French RoBERTa2RoBERTa (shared) fine-tuned on MLSUM FR for summarization. HuggingFace. https://huggingface.co/mrm8488/camembert2camembert_shared-finetuned-french-summarization.
