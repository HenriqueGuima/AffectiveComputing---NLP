from typing import Dict

from nlp.syntax import parse
from nlp.negation import NEGATIONS

POSITIVE = {
    "feliz", "felizmente", "alegre", "alegria", "bom", "boa", "melhor",
    "positivo", "sucesso", "gostar", "adorar", "conseguir", "aprovar", "aprovado",
    "conforto", "sorriso", "ótimo", "otimo", "excelente", "parabens",
    "incrível", "espetacular", "maravilhoso", "ganhar", "vencer", "benefício",
    "recomendar", "fácil", "rápido", "útil", "seguro", "confiança", "obrigado",
    "gratidão", "perfeito", "produtivo", "entusiasmado", "animado", "estupendo"
}

NEGATIVE = {
    "triste", "infelizmente", "raiva", "medo", "nojo", "má", "mau", "pior",
    "negativo", "falhar", "falhou", "chumbar", "chumbaram", "chumbou", "erros",
    "odiar", "problema", "dor", "mal", "péssimo", "pessimo", "terrível", 
    "horrível", "defeito", "difícil", "lento", "inútil", "inseguro", "perigo",
    "culpar", "reclamar", "desastre", "crise", "sofrer", "prejuízo", "ruim",
    "atraso", "confusão", "irritante", "vergonha", "desilusão", "frustração", "matar", "morte", "farto" , "infelizmente"
}

INTENSIFIERS = {
    "muito": 1.5,
    "bastante": 1.3,
    "demais": 1.4,
    "extremamente": 1.8,
    "completamente": 1.6,
    "totalmente": 1.6,
    "imensamente": 1.7,
    "pouco": 0.5,
    "ligeiramente": 0.7,
    "quase": 0.8,
    "apenas": 0.9
}

EMOTION_HINTS = {
    "alegria": {"feliz", "felizmente", "alegre", "alegria", "sorriso", "ótimo", "otimo", 
        "excelente", "maravilhoso", "entusiasmo", "celebrar", "rir", "contente"},
    "tristeza": {"triste", "infelizmente", "chorar", "choro", "luto", "melancolia", 
        "sozinho", "abandonado", "desânimo", "deprimido", "mágoa"},
    "raiva": {"raiva", "irritado", "zangado", "fúria", "ódio", "detestar", 
        "insuportável", "agressivo", "indignado", "nervoso", "matar", "morrer", "bater", "destruir"},
    "medo": {"medo", "assustado", "receio", "pânico", "terror", "ameaça", 
        "ansioso", "preocupado", "pavor", "tremendo"},
    "nojo": {"nojo", "repulsa", "asco", "nojento", "repugnante", "asqueroso", 
        "nauseabundo", "desprezo"},
    "surpresa": {"surpreendido", "surpresa", "espanto", "incrível", "inesperado", 
        "choque", "admirado", "pasmo", "estupefacto"}
}

INHERENT_POLARITY = {"infelizmente", "felizmente", "ótimo", "péssimo", "terrível", "horrível"}

def _token_stream(doc):
    for token in doc:
        yield token.text.lower(), token.lemma_.lower() if token.lemma_ else token.text.lower(), token.is_punct


def analyze_sentiment(doc) -> Dict[str, str]:
    """
    - Polaridade: positivo/negativo/neutro
    - Emoção de texto: alegria/tristeza/raiva/medo/nojo/surpresa/neutro
    """
    score = 0.0
    emotion_counts: Dict[str, int] = {k: 0 for k in EMOTION_HINTS.keys()}

    negate_window = 0
    intensifier = 1.0

    for text, lemma, is_punct in _token_stream(doc):
        # Reset de intensificador em pontuação
        if is_punct:
            intensifier = 1.0
            negate_window = 0
            continue

        # Ativar negação para próxima janela de 3 tokens de conteúdo
        if text in NEGATIONS:
            negate_window = 3
            continue

        # Intensificadores
        if text in INTENSIFIERS:
            intensifier = INTENSIFIERS[text]
            continue

        # Polaridade por léxico
        token_pos = text in POSITIVE or lemma in POSITIVE
        token_neg = text in NEGATIVE or lemma in NEGATIVE

        token_score = 0.0
        if token_pos:
            token_score = 1.0
        elif token_neg:
            token_score = -1.0

        # Aplicar negação local
        if negate_window > 0 and token_score != 0.0:
            if text not in INHERENT_POLARITY:
                token_score *= -1.0
            negate_window -= 1
        elif negate_window > 0:
            negate_window -= 1

        # Aplicar intensificador
        if token_score != 0.0:
            token_score *= intensifier
            intensifier = 1.0

        score += token_score

        # Contar pistas de emoção
        for emo, hints in EMOTION_HINTS.items():
            if text in hints or lemma in hints:
                emotion_counts[emo] += 1

    # Determinar polaridade
    if score > 0.5:
        polaridade = "positivo"
    elif score < -0.5:
        polaridade = "negativo"
    else:
        polaridade = "neutro"

    # Escolher emoção textual
    # Heurística: se positivo, favorecer alegria; se negativo, favorecer tristeza
    if polaridade == "positivo":
        if emotion_counts["alegria"] > 0:
            emocao = "alegria"
        else:
            # Caso positivo sem pista clara
            emocao = "neutro"
    elif polaridade == "negativo":
        if emotion_counts["tristeza"] > 0:
            emocao = "tristeza"
        elif max(emotion_counts.values(), default=0) > 0:
            # Escolher a emoção mais indicada pelas pistas
            emocao = max(emotion_counts.items(), key=lambda kv: kv[1])[0]
        else:
            emocao = "tristeza"
    else:
        # Neutro: se houver alguma pista, escolher a mais frequente; caso contrário, neutro
        if max(emotion_counts.values(), default=0) > 0:
            emocao = max(emotion_counts.items(), key=lambda kv: kv[1])[0]
        else:
            emocao = "neutro"

    return {"polaridade": polaridade, "emocao": emocao}

