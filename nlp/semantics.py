import re

PERSONAL_TOKENS = {
    "eu", "me", "meu", "mim", "comigo", "minha", "minhas", "meus",
    "ativado",
    "gravo", "noto", "amo", "aprecio", "omito", "termino",
    "vou", "prometi", "cozinhei", "comprei", "mostrei", "corri",
    "dormi", "liguei", "investiguei", "fico", "nasci", "quero", "-me"
}

# Corresponde a "eu <palavra>" onde a palavra contém apenas letras
PERSONAL_PHRASES = re.compile(r'\beu\s+[^\W\d_]+\b', re.IGNORECASE | re.UNICODE)

FACTUAL_MARKERS = {
    "segundo", "de acordo com", "conforme", "cientificamente",
    "estatisticamente", "comprovado", "demonstrado", "constatado",
    "pesquisa", "estudo", "dados", "relatório", "oficialmente",
    "evidência", "facto", "fato", "verdade", "documentado", "registrado"
}

OPINION_MARKERS = {
    "acho", "acredito", "penso", "parece", "creio", "imagino",
    "talvez", "provavelmente", "possivelmente", "supostamente",
    "opinião", "perspectiva", "ponto de vista", "julgo", "considero",
    "diria", "arrisco", "aposto", "suspeito"
}

SUBJECTIVE_ADJECTIVES = {
    "bonito", "feio", "bom", "mau", "melhor", "pior",
    "horrível", "maravilhoso", "terrível", "ótimo", "péssimo",
    "lindo", "horroroso", "fantástico", "espetacular", "medíocre"
}

def is_personal(doc):
    text_lower = doc.text.lower()

    if PERSONAL_PHRASES.search(text_lower):
        return True
    return any(token.text.lower() in PERSONAL_TOKENS for token in doc)

def is_factual(doc):
    """
    Determines if the text is a factual statement.
    Returns False for questions, commands, opinions, and personal statements.
    Returns True for objective, third-person declarative statements.
    """
    text = doc.text.strip()
    text_lower = text.lower()
    
    if "?" in text or "!" in text:
        return False
    
    if is_personal(doc):
        return False
    
    if any(marker in text_lower for marker in OPINION_MARKERS):
        return False
    
    if any(token.text.lower() in SUBJECTIVE_ADJECTIVES for token in doc):
        return False
    
    if any(marker in text_lower for marker in FACTUAL_MARKERS):
        return True
    
    return True
