#!/usr/bin/env python3

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import json
from ngramtools import NgramGenerator
import os
from pathlib import Path
from preprocessing import tokenize
import sys
from tqdm import tqdm
from util import alpha3convert


def main(args):
    data_path = Path("data/yle2024")
    ngrams_path = Path("ngrams")

    articles = list(data_path.glob("*.html"))

    checkpoint = args.checkpoint
    if args.checkpoint:
        articles = articles[(checkpoint * 10000):]
        generator = NgramGenerator.from_disk(ngrams_path)
    else:
        generator = NgramGenerator()

    for i, a in enumerate(tqdm(articles)):
        with open(a) as file:
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

        generator.update(tokens, lang_a3)

        if i + 1 % 10000 == 0 or i == len(articles):
            generator.to_disk(ngrams_path)
            print(f"Checkpoint 1: {i + 1} articles processed.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", "--checkpoint", type=int)
    args = parser.parse_args()

    main(args)
