#!/usr/bin/env python3

import requests
from tqdm import tqdm

def main():
    url_template = "https://yle.fi/a/74-{idx}"
    file_template = "data/yle2024/74-{idx}.html"

    first_2024 = 20067251
    most_recent = 20132993  # Fri 20 Dec 17:52:50 EET 2024 
    indices = range(first_2024, most_recent + 1)

    with requests.Session() as session:
        for idx in tqdm(indices):
            url = url_template.format(idx=idx)
            with session.get(url, stream=True) as r:
                if r.status_code != 200:
                    continue
                filename = file_template.format(idx=idx)
                with open(filename, "wb") as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)

if __name__ == "__main__":
    main()
