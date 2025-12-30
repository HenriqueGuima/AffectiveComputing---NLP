import os
import sys
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

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
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=callback):
            
            while True:
                data = audio_queue.get()
                if recognizer.AcceptWaveform(data):
                    # Extrai o texto do JSON retornado pelo Vosk
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        print(f"Transcrição Local: {text}")
                        return text 
                
    except Exception as e:
        print(f"Erro no processamento de áudio local: {e}")
        return ""


def get_text_input():
    print("\n------------")
    print("1. Digitar texto (Teclado)")
    print("2. Falar (Microfone)")
    
    opcao = input("Escolha uma opção (1 ou 2): ").strip()
    
    if opcao == '2':
        resultado = get_audio_input()
        # Se falhar a voz, cai para o teclado como backup
        if not resultado:
            return input("Falha na voz. Introduza via teclado: ")
        return resultado
    else:
        return input("Introduza uma frase: ")