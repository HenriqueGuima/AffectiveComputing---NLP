PERSONAL_TOKENS = {
    "eu", "me", "meu",
    "ativado",
    "gravo", "noto", "amo", "aprecio", "omito", "termino",
    "vou", "prometi", "cozinhei", "comprei", "mostrei", "corri",
    "dormi", "liguei", "investiguei", "fico", "nasci", "quero", "-me"
}

PERSONAL_PHRASES = {
    "eu gravo", "eu noto", "eu amo", "eu aprecio", "eu termino"
}

def is_personal(doc):
    text_lower = doc.text.lower()
    if any(phrase in text_lower for phrase in PERSONAL_PHRASES):
        return True
    return any(token.text.lower() in PERSONAL_TOKENS for token in doc)

def is_factual(doc):
    return not is_personal(doc)
