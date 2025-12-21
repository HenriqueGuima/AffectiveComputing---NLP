from spellchecker import SpellChecker

spell = SpellChecker(language="pt")

def correct_text(text):
    words = text.split()
    corrected_words = []

    for word in words:
        corrected = spell.correction(word)
        corrected_words.append(corrected if corrected else word)

    return " ".join(corrected_words)
