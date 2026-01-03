from preprocessing.spellcheck import correct_text
from nlp.syntax import parse
from nlp.negation import has_negation
from nlp.semantics import is_personal
from nlp.type import detect_type
from nlp.sentiment import analyze_sentiment

from core.result import empty_result
from ui.input_controller import select_input

def main():
    first_run = True
    while True:
        result = empty_result()

        if not first_run:
            resposta = input("\n\nDeseja continuar? (s/n): ").strip().lower()
            if resposta in {"n", "nao", "não", ":q", "q"}:
                print("\n A sair...\n")
                break

        first_run = False

        text, source = select_input()

        if isinstance(text, str) and text.strip() == ':q' or (not text):
            print("\n A sair...\n")
            break

        result["frase_original"] = text

        corrected = correct_text(text)
        result["frase_corrigida"] = corrected
        
        doc = parse(corrected)

        result["negacao"] = has_negation(doc)
        result["pessoal"] = is_personal(doc)
        result["tipo"] = detect_type(result["frase_corrigida"], result["negacao"])

        sentiment = analyze_sentiment(doc)
        result["polaridade"] = sentiment.get("polaridade", "")
        result["emocao_texto"] = sentiment.get("emocao", "")

        print("\n--- RESULTADO ---\n")

        for key, value in result.items():
            if isinstance(value, bool):
                if not value:
                    continue
            else:
                if not value:
                    continue

            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
