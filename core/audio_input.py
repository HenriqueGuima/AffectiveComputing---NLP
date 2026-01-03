import os
import sys
import queue
import json
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import warnings
warnings.filterwarnings("ignore")

from voice.emotionRecognizer import analisar_emocao

audio_queue = queue.Queue()

def callback(indata, frames, time_info, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))


def _process_result(recognizer, buffer_frase, texto=""):
    texto = (texto or "").strip()

    if not texto:
        texto = json.loads(recognizer.FinalResult()).get("text", "").strip()

    if not texto:
        print("\n[INFO] Sem transcrição disponível.")
        return ""

    audio_completo = b"".join(buffer_frase)
    emocao = analisar_emocao(audio_completo) if audio_completo else ""

    print(f"Texto: {texto}")
    print(f"Sentimento: {emocao}")

    return texto

def get_audio_input(max_seconds: float = 10.0):
    base_path = os.path.dirname(__file__)
    model_path = os.path.join(base_path, "model")

    if not os.path.exists(model_path):
        print(f"\n[ERRO] Modelo não encontrado em: {model_path}")
        return ""

    try:
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)

        print("\n[VOSK LOCAL] A escutar... Fala agora.")
        print(f"(Timeout: {max_seconds:.0f}s)")

        start_time = time.time()

        with sd.RawInputStream(
            samplerate=16000,
            blocksize=16000,
            dtype="int16",
            channels=1,
            callback=callback
        ):
            buffer_frase = []

            while True:
                # timeout to break the loop
                if (time.time() - start_time) > max_seconds:
                    print("\n[INFO] Timeout atingido.")
                    return _process_result(recognizer, buffer_frase)

                data = audio_queue.get()
                buffer_frase.append(data)

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    texto = result.get("text", "").strip()

                    if texto:
                        return _process_result(recognizer, buffer_frase, texto)

    except Exception as e:
        print(f"Erro no processamento de áudio local: {e}")
        return ""
