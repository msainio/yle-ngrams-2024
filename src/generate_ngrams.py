#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
from nltk.util import bigrams, trigrams
import os
from pathlib import Path
from preprocessing import tokenize
from tqdm import tqdm
from util import NgramCounter, alpha3convert, serialize


def main():
    data_path = Path("data/yle2024")
    ngrams_path = Path("ngrams")

    ngram_counter = NgramCounter()
    
    for file in tqdm(data_path.glob("*.html")):
        with open(file) as fp:
            soup = BeautifulSoup(fp, features="lxml")

        texts = []
        for p in soup.section.find_all("p"):
            if p["class"][-1] == "yle__article__paragraph":
                texts.append(p.get_text(" ", strip=True))

        script = soup.find_all("script")[-1]
        obj = json.loads("=".join(script.string.split("=")[1:]))
        lang = obj["pageData"]["article"]["language"]

        tokens = tokenize(texts, lang)
        lang_a3 = alpha3convert(lang)

        ngram_counter.update(tokens, lang_a3, "word_fd")
        ngram_counter.update(bigrams(tokens), lang_a3, "bigram_fd")
        ngram_counter.update(trigrams(tokens), lang_a3, "trigram_fd")

    for l in ngram_counter.get_langs():
        counters = ngram_counter.get_counters(l)

        for k, v in counters.items():
            output_dir = ngrams_path / l
            os.makedirs(output_dir, exist_ok=True)
            with open(output_dir / f"{k}.json", "w") as fp:
                json.dump(serialize_counter(v), fp, ensure_ascii=False)


if __name__ == "__main__":
    main()
