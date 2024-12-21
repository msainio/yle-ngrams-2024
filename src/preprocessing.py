from itertools import chain
from spacy.util import get_lang_class
from uralicNLP import tokenizer as uralic_tokenizer


class Uralic:
    def __init__(self):
        self.tokenizer = UralicTokenizer()


class UralicTokenizer:
    def pipe(self, texts):
        docs = []
        for text in texts:
            tokens = uralic_tokenizer.words(text)
            docs.append([UralicToken(token) for token in tokens])
        return docs


class UralicToken:
    def __init__(self, text):
        self.text = text


def tokenize(texts, lang):
    try:
        nlp = get_lang_class(lang)()
    except:
        nlp = Uralic()

    docs = nlp.tokenizer.pipe(texts)
    tokens = [[tok.text for tok in doc] for doc in docs]

    return list(chain.from_iterable(tokens))
