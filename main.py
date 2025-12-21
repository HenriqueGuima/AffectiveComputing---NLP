from core.text_input import get_text_input
from preprocessing.spellcheck import correct_text
from nlp.syntax import parse
from nlp.negation import has_negation
from nlp.semantics import is_personal

def main():
    text        = get_text_input()
    corrected   = correct_text(text)
    doc         = parse(corrected)
    negation    = has_negation(doc)
    personal    = is_personal(doc)

    print("\n--- RESULTADO ---")
    print("Original :", text)
    print("Corrigida:", corrected)
    print("Negação  :", negation)
    print("Pessoal :", personal)

if __name__ == "__main__":
    main()
