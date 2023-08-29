import re

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

FRENCH_SUMMARIZER = "mrm8488/camembert2camembert_shared-finetuned-french-summarization"
ENGLISH_SUMMARIZER = "csebuetnlp/mT5_multilingual_XLSum"


class NLP:
    def __init__(self, langs: list) -> None:
        self.WHITESPACE_HANDLER = lambda k: re.sub(
            r"\s+", " ", re.sub("\n+", " ", k.strip())
        )
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            SpinnerColumn(),
            TimeElapsedColumn(),
        ) as progress:
            # ENGLISH MODEL
            if "en" in langs:
                progress.add_task(description="[red]Downloading English model...")
                print("\n\nEnglish model: {}".format(ENGLISH_SUMMARIZER))
                self.english_tokenizer = AutoTokenizer.from_pretrained(
                    ENGLISH_SUMMARIZER
                )
                self.english_model = AutoModelForSeq2SeqLM.from_pretrained(
                    ENGLISH_SUMMARIZER
                )

            # FRENCH MODEL
            if "fr" in langs:
                progress.add_task(description="[blue]Downloading French model...")
                print("\n\nFrench model: {}".format(FRENCH_SUMMARIZER))
                self.french_tokenizer = AutoTokenizer.from_pretrained(FRENCH_SUMMARIZER)
                self.french_model = AutoModelForSeq2SeqLM.from_pretrained(
                    FRENCH_SUMMARIZER
                )

    def __call__(self, text, lang):
        # MAKE INFERENCE WITH FRENCH MODEL
        if lang == "fr" and self.french_tokenizer and self.french_model:
            input_ids = self.french_tokenizer(
                [self.WHITESPACE_HANDLER(text)],
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=512,
            )["input_ids"]

            try:
                output_ids = self.french_model.generate(
                    input_ids=input_ids,
                    max_length=84,
                    no_repeat_ngram_size=2,
                    num_beams=4,
                )[0]
            except Exception as e:
                return e
            else:
                summary = self.french_tokenizer.decode(
                    output_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False,
                )
                return summary

        # MAKE INFERENCE WITH ENGLISH MODEL
        if lang == "en" and self.english_model and self.english_tokenizer:
            input_ids = self.english_tokenizer(
                [self.WHITESPACE_HANDLER(text)],
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=512,
            )["input_ids"]

            try:
                output_ids = self.english_model.generate(
                    input_ids=input_ids,
                    max_length=84,
                    no_repeat_ngram_size=2,
                    num_beams=4,
                )[0]
            except Exception as e:
                return e
            else:
                summary = self.english_tokenizer.decode(
                    output_ids,
                    skip_special_tokens=True,
                    clean_up_tokenization_spaces=False,
                )
                return summary
