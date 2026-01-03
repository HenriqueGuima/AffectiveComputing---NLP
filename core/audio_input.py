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