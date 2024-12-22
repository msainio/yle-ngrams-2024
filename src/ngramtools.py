from pathlib import Path
import json
from nltk.collocations import TrigramCollocationFinder
from nltk.probability import FreqDist
import os

_fd_names = ["word_fd", "bigram_fd", "wildcard_fd", "trigram_fd"]


class NgramContainer:

    def __init__(self, finders=None):
        if not finders:
            finders = {}

        self.finders = finders

    @classmethod
    def from_disk(cls, path):
        path_obj = Path(path)

        finders = {}
        for lang_dir in path_obj.iterdir():
            if lang_dir.is_dir():
                lang = str(lang_dir)
                finders[lang] = finder_from_disk(lang_dir)

        return cls(finders)

    def update(self, words, lang):
        finder_seq = TrigramCollocationFinder.from_words(words)

        if lang not in self.finders.keys():
            self.finders[lang] = finder_seq
        else:
            finder_all = self.finders[lang]

            for name, fd_seq in vars(finder_seq).items():
                if name != "N":
                    fd_all = getattr(finder_all, name)
                    fd_all.update(fd_seq)
                    setattr(finder_all, name, fd_all)

            finder_all.N = finder_all.word_fd.N()

    def serialize(self):
        return {k: serialize_finder(v) for k, v in self.finders.items()}

    def to_disk(self, path):
        for lang, finder in self.serialize().items():
            output_dir = path / lang
            os.makedirs(output_dir, exist_ok=True)

            for name, fd in finder.items():
                with open(output_dir / f"{name}.json", "w") as file:
                    json.dump({name: fd}, file, ensure_ascii=False)

    def get_finders(self):
        return self.finders


def serialize_finder(finder):
    ser_finder = {}
    for name, fd in vars(finder).items():
        if name == "N":
            continue
        if name == "ngram_fd":
            name = "trigram_fd"

        ser_fd = [[(list(e) if isinstance(e, tuple) else e), c]
                  for e, c in fd.items()]
        ser_finder[name] = ser_fd

    return ser_finder


def deserialize_finder(ser_finder):
    fdists = {}

    for name, ser_fd in ser_finder.items():
        elements = [((tuple(e) if isinstance(e, list) else e), c)
                    for e, c in ser_fd]
        fdists[name] = FreqDist(elements)

    return TrigramCollocationFinder(**fdists)


def finder_from_disk(path):
    path_obj = Path(path)

    ser_fdists = {}
    for name in _fd_names:
        file_path = path_obj / f"{name}.json"

        with open(file_path) as file:
            ser_fd = json.load(file)

            for k, v in ser_fd.items():
                ser_fdists[k] = v

    return deserialize_finder(ser_fdists)
