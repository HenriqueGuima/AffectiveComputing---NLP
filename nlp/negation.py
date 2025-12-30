NEGATIONS = {"não", "nunca", "jamais", "nem", "nada", 
            "ninguém", "nenhum", "nenhuma", "tampouco", "sem"}

def has_negation(doc):
    return any(token.text.lower() in NEGATIONS for token in doc)
