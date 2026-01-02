import torch
import numpy as np
import librosa
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
import warnings
warnings.filterwarnings("ignore")

MODEL_NAME = "superb/wav2vec2-base-superb-er"

feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_NAME)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_NAME)
model.gradient_checkpointing_enable() 

def analisar_emocao(audio_bytes):
    """
    Recebe os bytes de áudio (do sounddevice), converte e prediz a emoção.
    """
    try:
        # 1. Converter bytes brutos (int16) para float32 numpy array
        # O modelo espera áudio normalizado entre -1 e 1
        audio_int16 = np.frombuffer(audio_bytes, dtype=np.int16)
        audio_float = audio_int16.astype(np.float32) / 32768.0

        # O modelo geralmente foi treinado com áudios de 1 segundo ou mais.
        # Se for muito curto, pode dar erro ou ser impreciso.
        if len(audio_float) < 4000: # Ignorar áudios minúsculos
            return "Indefinido"

        # 2. Processar entrada
        inputs = feature_extractor(audio_float, sampling_rate=16000, return_tensors="pt", padding=True)

        # 3. Predição
        with torch.no_grad():
            logits = model(**inputs).logits

        # 4. Pegar a etiqueta com maior pontuação
        predicted_ids = torch.argmax(logits, dim=-1)
        labels = [model.config.id2label[_id] for _id in predicted_ids.tolist()]
        
        # Traduzindo para PT (O modelo retorna em inglês 'hap', 'sad', 'neu', 'ang')
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