NEGATIONS = {"não", "nunca", "jamais", "nem"}

def has_negation(doc):
    return any(token.text.lower() in NEGATIONS for token in doc)
