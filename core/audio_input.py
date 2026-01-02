import os
import sys
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import warnings
warnings.filterwarnings("ignore")

from voice.emotionRecognizer import analisar_emocao

audio_queue = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

def get_audio_input():
    # Define o caminho para a pasta do modelo relativo a este ficheiro 
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, "model")

    if not os.path.exists(model_path):
        print(f"\n[ERRO] Modelo não encontrado em: {model_path}")
        return ""

    try:
        # Inicializa o modelo (Português) e o reconhecedor a 16000Hz
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)

        print("\n[VOSK LOCAL] A escutar... Fala agora.")

        # Inicia a captura do fluxo de áudio bruto
        with sd.RawInputStream(samplerate=16000, blocksize=16000, dtype='int16',
                               channels=1, callback=callback):
            
            # (Dentro do loop do get_audio_input)
            buffer_frase = [] # Lista para guardar o áudio da frase atual

            while True:
                data = audio_queue.get()
                buffer_frase.append(data) # Acumula o áudio
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    texto = result.get("text", "")
                    
                    if texto:
                        # Juntar o buffer de áudio num único bloco de bytes
                        audio_completo = b''.join(buffer_frase)
                        
                        # Analisar a emoção desse bloco
                        emocao = analisar_emocao(audio_completo)
                        
                        print(f"Texto: {texto}")
                        print(f"Sentimento: {emocao}")
                        
                        buffer_frase = []
                        
                        return texto 
                
    except Exception as e:
        print(f"Erro no processamento de áudio local: {e}")
        return ""


def get_text_input():
    print("\n\n------------\n")
    print("1. Introduzir texto (Teclado)")
    print("2. Falar (Microfone)")
    print("\n\nIntroduzir ':q' para sair.")
    print("\n------------\n")

    while True:
        opcao = input("Escolha uma opção (1 ou 2): ").strip().lower()

        # Permitir saída direta pelo menu
        if opcao in {":q", "q"}:
            return ":q", 'keyboard'

        # Pedir de novo se não for dígito
        if not opcao.isdigit():
            print("Opção inválida. Por favor, introduza 1 ou 2.")
            continue

        if opcao == '2':
            resultado = get_audio_input()

            # Fallback to keyboard
            if not resultado:
                return input("\n\nFalha na voz. Introduza via teclado: "), 'keyboard'
            
            return resultado, 'microfone'
        elif opcao == '1':
            return input("Introduza uma frase: "), 'keyboard'
        else:
            print("Opção inválida. Por favor, escolha 1 ou 2.")
            continue