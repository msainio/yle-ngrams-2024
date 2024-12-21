from collections import Counter


class NgramCounter:

    def __init__(self):
        self.counters = {}
        self.langs = set()

    def update(self, ngrams, lang, degree):
        if lang not in self.langs:
            self.counters[lang] = {
                    "word_fd": Counter(),
                    "bigram_fd": Counter(),
                    "trigram_fd": Counter()
                    }
            self.langs.add(lang)
        self.counters[lang][degree].update(ngrams)

    def get_counters(self, lang):
        return self.counters[lang]

    def get_langs(self):
        return self.langs


def alpha3convert(alpha2):
    mapping = {
        "en": "eng",
        "fi": "fin",
        "ru": "rus",
        "se": "sme",
        "smn": "smn",
        "sms": "sms",
        "uk": "ukr"
        }
    return mapping[alpha2]


def deserialize(counts):
    return Counter([((tuple(e) if type(e) is list else e), n)
                    for e, n in counts])


def serialize(counter):
    return [[(list(e) if type(e) is tuple else e), n]
            for e, n in counter.items()]
