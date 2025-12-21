import spacy

_nlp = None

def _ensure_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("pt_core_news_lg")
        except Exception:
            try:
                _nlp = spacy.load("pt_core_news_sm")
            except Exception:
                _nlp = spacy.blank("pt")
    return _nlp


def parse(text):
    """Return a spaCy Doc for the given text (used by main, negation, semantics)."""
    return _ensure_nlp()(text)


def analyze_syntax(text):
    nlp = _ensure_nlp()
    doc = nlp(text)

    return {
        "tokens": [token.text for token in doc],
        "pos": [token.pos_ for token in doc],
        "lemmas": [token.lemma_ for token in doc]
    }
