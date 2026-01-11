import torch
import numpy as np
import librosa
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification
import warnings
warnings.filterwarnings("ignore")

# Modelo de reconhecimento de emoções guardado na pasta ./model_emotion/
MODEL_NAME = "./model_emotion/"

# Carregar o extrator de características
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(
    MODEL_NAME, 
    local_files_only=True
)
# Carregar o modelo Wav2Vec2 para classificação de sequências (emoções)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_NAME,local_files_only=True)
model.gradient_checkpointing_enable() 

def analisar_emocao(audio_bytes):

    try:
        # Converter os bytes brutos do áudio para um array NumPy
        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)

        # Normalizar o áudio , converte de int16 para float32 num intervalo [-1.0, 1.0]
        audio_float = audio_int16.astype(np.float32) / 32768.0

        if len(audio_float) < 4000: 
            return "Indefinido"

        # Processar entrada
        inputs = feature_extractor(audio_float, sampling_rate=16000, return_tensors="pt", padding=True)

        # Predição
        with torch.no_grad():
            logits = model(**inputs).logits

        # Pegar a etiqueta com maior pontuação
        predicted_ids = torch.argmax(logits, dim=-1)
        labels = [model.config.id2label[_id] for _id in predicted_ids.tolist()]
        
        traducao = {
            "neu": "Neutro",
            "hap": "Alegria",
            "ang": "Raiva",
            "sad": "Tristeza",
            "sur": "Surpresa", 
            "fea": "Medo"
        }
        
        emocao_en = labels[0]
        return traducao.get(emocao_en, emocao_en)

    except Exception as e:
        print(f"Erro na análise de emoção: {e}")
        return "Erro"