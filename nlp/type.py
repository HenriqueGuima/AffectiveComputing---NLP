from helpers.question_words import QUESTION_WORDS

# If sentence ends in ? means question
# If negation true means negation
# Default is affirmation
# If by mistake or the question mark is in the middle of the sentence added normal words that means questions
def detect_type(text: str, negation: bool) -> str:
    text = (text or "").strip()
    lower = text.lower()

    if text.endswith("?"):
        return "pergunta"

    if "!" in text:
        return "exclamacao"

    if negation:
        return "negacao"

    return "afirmacao"