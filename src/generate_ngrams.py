#!/usr/bin/env python3

import aiofiles
import asyncio
from asyncio import Semaphore
from bs4 import BeautifulSoup
import json
from collections import Counter
from collocations import MultiCollocationFinder
from pathlib import Path
from preprocessing import tokenize
from tqdm.asyncio import tqdm_asyncio
from util import ensure_alpha3


async def get_ngrams(filename, finder, semaphore):
    async with semaphore:
        async with aiofiles.open(filename) as file:
            markup = await file.read()

    soup = BeautifulSoup(markup, features="lxml")

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
    lang_a3 = ensure_alpha3(lang)
    finder.update(tokens, lang_a3)

    return lang_a3


async def main():
    data_path = Path("data/yle2024")
    ngrams_path = Path("ngrams")

    mcf = MultiCollocationFinder()
    sem = Semaphore(100)

    tasks = [get_ngrams(file, mcf, sem) for file in data_path.glob("*.html")]
    lang_codes = await tqdm_asyncio.gather(*tasks)

    mcf.to_disk(ngrams_path)

    print("Articles processed:")
    print(Counter(lang_codes).most_common())

if __name__ == "__main__":
    asyncio.run(main())
