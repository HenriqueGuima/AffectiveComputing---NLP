from core.audio_input import get_audio_input
from core.text_input import get_text_input

def select_input():
    print("\n\n------------\n")
    print("\n1. Introduzir texto (Teclado)")
    print("2. Falar (Microfone)")
    print("\nIntroduzir ':q' para sair.\n")
    print("\n\n------------\n")

    while True:
        opcao = input("Escolha uma opção (1 ou 2): ").strip().lower()

        if opcao in {":q", "q"}:
            return ":q", "keyboard"

        if opcao == "1":
            return get_text_input(), "keyboard"

        if opcao == "2":
            texto = get_audio_input()
            if not texto:
                return get_text_input(), "keyboard"
            return texto, "microfone"

        print("Opção inválida.")
