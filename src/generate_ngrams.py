#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
from ngramtools import NgramContainer
from pathlib import Path
from preprocessing import tokenize
from tqdm import tqdm
from util import alpha3convert


def main(args):
    data_path = Path("data/yle2024")
    ngrams_path = Path("ngrams")

    container = NgramContainer()

    for file_name in tqdm(data_path.glob("*.html")):
        with open(file_name) as file:
            soup = BeautifulSoup(file, features="lxml")

        texts = []
        for p in soup.section.find_all("p"):
            if p["class"][-1] == "yle__article__paragraph":
                texts.append(p.get_text(" ", strip=True))

        script = soup.find_all("script")[-1]
        obj = json.loads("=".join(script.string.split("=")[1:]))
        lang = obj["pageData"]["article"]["language"]

        tokens = tokenize(texts, lang)
        lang_a3 = alpha3convert(lang)

        container.update(tokens, lang_a3)

    container.to_disk(ngrams_path)


if __name__ == "__main__":
    main()
