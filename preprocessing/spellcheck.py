import re
from spellchecker import SpellChecker

spell = SpellChecker(language="pt")

def correct_text(text):
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    corrected_tokens = []

    for token in tokens:
        if token.isalpha():
            corrected = spell.correction(token)
            if corrected:
                if token.isupper():
                    corrected = corrected.upper()
                elif token[0].isupper():
                    corrected = corrected.capitalize()
                corrected_tokens.append(corrected)
            else:
                corrected_tokens.append(token)
        else:
            corrected_tokens.append(token)
    return "".join(
        (" " + t if i > 0 and t[0].isalnum() and corrected_tokens[i-1][-1].isalnum() else t)
        for i, t in enumerate(corrected_tokens)
    ).strip()
