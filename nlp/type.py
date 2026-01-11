from helpers.question_words import QUESTION_WORDS


# Se a frase terminar em ? significa pergunta
# Se a negação for true significa negação
# Se por erro o ponto de interrogação estiver no meio da frase com palavras normais seguidas, significa pergunta
def detect_type(text: str, negation: bool) -> str:
    text = (text or "").strip()
    lower = text.lower()

    if text.endswith("?"):
        return "pergunta"
    
    if any(lower.startswith(q) for q in QUESTION_WORDS):
        return "pergunta"

    if "!" in text:
        return "exclamacao"

    if negation:
        return "negacao"

    return "afirmacao"