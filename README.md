# Yle *n*-grams 2024

## Overview

This repository contains code and data for studying word occurrences in news articles published by [Yle – the Finnish Broadcasting Company](https://yle.fi/) in 2024. The data consist of *n*-gram distribution
frequencies generated from 58,964 articles published by Yle between January 1
and December 20, 2024.

There are *n*-grams for eight different languages:

| Language      | Num. articles |
|---------------|--------------:|
| Finnish       | 51,895        |
| Russian       | 3,039         |
| English       | 2,500         |
| Ukrainian     | 1,005         |
| Northern Sámi | 383           |
| Karelian      | 60            |
| Inari Sámi    | 46            |
| Skolt Sámi    | 46            |

The *n*-gram frequency distributions are serialized in JSON format. Due to the
size of the Finnish data, the Finnish files are supplied in ZIP format. You
can run the `scripts/decompress.sh` file to decompress them for analysis.

## Usage

You can use the `get_collocation_finder` and `get_word_fd` functions from
`src/collocations.py` to load *n*-gram frequency distributions to memory and
construct an NLTK `FreqDist`, `BigramCollocationFinder` or
`TrigramCollocationFinder` object. For general information on how to use these
objects, see NLTK example usage for
[frequency distributions](https://www.nltk.org/howto/probability.html#freqdist)
and
[collocation finders](https://www.nltk.org/howto/collocations.html#collocations).

### Example usage

#### Collocations

```python
>>> from nltk.metrics import BigramAssocMeasures as bam
>>> from src.collocations import get_collocation_finder
>>>
>>> # Construct bigram collocation finder from disk
>>> finder = get_collocation_finder(path="ngrams/eng", n=2)
>>>
>>> # Ignore bigrams that occur only once or contain capitalized words
>>> finder.apply_freq_filter(2)
>>> finder.apply_word_filter(lambda w: w != w.lower())
>>>
>>> # Top ten collocations measured using PMI
>>> finder.nbest(bam.pmi, 10)
[('forcible', 'confinement'), ('maple', 'syrup'), ('spam', 'folder'),
('swamp', 'soccer'), ('514', '214'), ('cosmic', 'soundscapes'),
('furry', 'seafarer'), ('inadequately', 'redacted'),
('vitro', 'fertilisation'), ('cerebral', 'thrombosis')]
```

#### Frequency distributions

```python
>>> from src.collocations import get_word_fd
>>>
>>> # Construct frequency distribution from disk
>>> word_fd = get_word_fd(path="ngrams/eng")
>>>
>>> # Top ten most frequent words
>>> word_fd.most_common(10)
[('the', 54109), (',', 47397), ('.', 43926), ('to', 26973), ('of', 25880),
('in', 22559), ('and', 18245), ('a', 17318), ('"', 12134), ('that', 12052)]
```
