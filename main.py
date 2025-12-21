from core.text_input import get_text_input
from preprocessing.spellcheck import correct_text

def main():
    text        = get_text_input()
    corrected   = correct_text(text)

    print("Original:", text)
    print("Corrigida:", corrected)

if __name__ == "__main__":
    main()
