import spacy

_nlp = spacy.load("pt_core_news_lg")

def parse(text):
    """Return a spaCy Doc for the given text (used by main, negation, semantics)."""
    return _nlp(text)

def analyze_syntax(text):
    doc = _nlp(text)

    return {
        "tokens": [token.text for token in doc],
        "pos": [token.pos_ for token in doc],
        "lemmas": [token.lemma_ for token in doc]
    }
