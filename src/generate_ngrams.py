#!/usr/bin/env python3

from bs4 import BeautifulSoup
import json
from ngramtools import NgramContainer
from pathlib import Path
from preprocessing import tokenize
from tqdm import tqdm
from util import alpha3convert


def main():
    data_path = Path("data/yle2024")
    ngrams_path = Path("ngrams")

    container = NgramContainer()

    for file_name in tqdm(data_path.glob("*.html")):
        with open(file_name) as file:
            soup = BeautifulSoup(file, features="lxml")

        texts = []

        metadata = json.loads(soup.find(id="json-ld-microdata").string)
        for k, v in metadata["@graph"][0].items():
            if k in ("headline", "description"):
                texts.append(v)

        for p in soup.section.find_all("p", class_="yle__article__paragraph"):
            if not p.em:
                texts.append(p.get_text(" ", strip=True))

        script = soup.body.find("script", type="text/javascript") 
        obj = json.loads(script.string.split("=", 1)[1])
        lang = obj["pageData"]["article"]["language"]

        tokens = tokenize(texts, lang)
        lang_a3 = alpha3convert(lang)

        container.update(tokens, lang_a3)

    container.to_disk(ngrams_path)


if __name__ == "__main__":
    main()
