from nltk.collocations import TrigramCollocationFinder
from nltk.probability import FreqDist


class NgramGenerator:

    def __init__(self):
        self.finders = {}

    def update(self, words, language):
    finder_seq = TrigramCollocationFinder.from_words(words)

    if language not in self.finders.keys():
        self.finders[language] = finder_seq
    else:
        finder_all = self.finders[language]
        for key, value in vars(finder_seq).items():
            if key != "N":
                fd = getattr(finder_all, key)
                setattr(finder_all, key, fd.update(value))
        finder_all.N = finder_all.word_fd.N()

    def serialize(self):
        return {k: serialize_finder(v) for k, v in self.finders.items()}

    def get_finders(self):
        return self.finders


def serialize_finder(finder):
    ser_finder = {}
    for key, value in vars(finder).items():
        if key != "N":
            ser_fd = [[(list(e) if type(e) is tuple else e), c]
                      for e, c in value.items()]
        ser_finder[key] = ser_fd
    return ser_finder


def deserialize_finder(ser_finder):
    fdists = {}
    for key, value in ser_finder.items():
        fdists[key] = FreqDist([((tuple(e) if type(e) is list else e), c)
                                for e, c in value])
    return TrigramCollocationFinder(**fdists)
