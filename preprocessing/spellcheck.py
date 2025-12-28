import re
from spellchecker import SpellChecker

spell = SpellChecker(language="pt")

# Added new logic
# Now the final ponctuation is added in the end of the sentence
def correct_text(text):
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    corrected_tokens = []

    for token in tokens:
        if token.isalpha():
            corrected = spell.correction(token)
            corrected_tokens.append(corrected if corrected else token)
        else:
            corrected_tokens.append(token)

    return "".join(
        (" " + t if i > 0 and t.isalpha() and corrected_tokens[i-1].isalpha() else t)
        for i, t in enumerate(corrected_tokens)
        ).strip()
