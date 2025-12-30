from preprocessing.spellcheck import correct_text
from nlp.syntax import parse
from nlp.negation import has_negation
from nlp.semantics import is_personal
from nlp.type import detect_type

#from core.text_input import get_text_input
from core.audio_input import get_text_input

from core.result import empty_result

def main():
    result = empty_result()

    text = get_text_input()
    result["frase_original"] = text

    corrected = correct_text(text)
    result["frase_corrigida"] = corrected
    
    doc = parse(corrected)

    result["negacao"] = has_negation(doc)
    result["pessoal"] = is_personal(doc)
    result["tipo"] = detect_type(result["frase_corrigida"], result["negacao"])

    print("\n--- RESULTADO ---")
    for key, value in result.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
