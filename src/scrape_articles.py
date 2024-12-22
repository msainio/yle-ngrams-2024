#!/usr/bin/env python3

from pathlib import Path
import os
import requests
from tqdm import tqdm


def main():
    output_dir = Path("data/yle2024")
    os.makedirs(output_dir, exist_ok=True)

    url_template = "https://yle.fi/a/74-{idx}"
    filename_template = "74-{idx}.html"

    idx_first_2024 = 20067251
    idx_most_recent = 20132993  # Fri 20 Dec 17:52:50 EET 2024 
    indices = range(idx_first_2024, idx_most_recent + 1)

    with requests.Session() as session:
        for idx in tqdm(indices):
            url = url_template.format(idx=idx)
            with session.get(url, stream=True) as r:
                if r.status_code != 200:
                    continue
                filename = filename_template.format(idx=idx)
                with open(output_dir / filename, "wb") as file:
                    for chunk in r.iter_content(chunk_size=128):
                        file.write(chunk)


if __name__ == "__main__":
    main()
