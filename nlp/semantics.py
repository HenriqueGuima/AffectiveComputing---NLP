import re

PERSONAL_TOKENS = {
    "eu", "me", "meu",
    "ativado",
    "gravo", "noto", "amo", "aprecio", "omito", "termino",
    "vou", "prometi", "cozinhei", "comprei", "mostrei", "corri",
    "dormi", "liguei", "investiguei", "fico", "nasci", "quero", "-me"
}

# Corresponde a "eu <palavra>" onde a palavra contém apenas letras
PERSONAL_PHRASES = re.compile(r'\beu\s+[^\W\d_]+\b', re.IGNORECASE | re.UNICODE)

def is_personal(doc):
    text_lower = doc.text.lower()

    if PERSONAL_PHRASES.search(text_lower):
        return True
    return any(token.text.lower() in PERSONAL_TOKENS for token in doc)

def is_factual(doc):
    return not is_personal(doc)
