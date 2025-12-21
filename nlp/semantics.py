def is_personal(doc):
    return any(token.pos_ == "PRON" and token.text.lower() in {"eu", "me", "meu"} for token in doc)

def is_factual(doc):
    return not is_personal(doc)
