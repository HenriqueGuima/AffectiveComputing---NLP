from typing import Dict

from nlp.syntax import parse
from nlp.negation import NEGATIONS

# TODO expandir com SentiLex-PT/OpLexicon ou dicionários próprios.
POSITIVE = {
    "feliz", "felizmente", "alegre", "alegria", "bom", "boa", "melhor",
    "positivo", "sucesso", "gostar", "adorar", "conseguir", "aprovar", "aprovado",
    "conforto", "sorriso", "ótimo", "otimo", "excelente", "parabéns", "parabens"
}

NEGATIVE = {
    "triste", "infelizmente", "raiva", "medo", "nojo", "má", "mau", "pior",
    "negativo", "falhar", "falhou", "chumbar", "chumbaram", "chumbou", "erros",
    "odiar", "problema", "dor", "mal", "péssimo", "pessimo"
}

INTENSIFIERS = {
    "muito": 1.5,
    "bastante": 1.3,
    "demais": 1.4,
    "pouco": 0.5
}

EMOTION_HINTS = {
    "alegria": {"feliz", "felizmente", "alegre", "alegria", "sorriso", "ótimo", "otimo", "excelente"},
    "tristeza": {"triste", "infelizmente", "chorar", "choro"},
    "raiva": {"raiva", "irritado", "zangado"},
    "medo": {"medo", "assustado", "receio"},
    "nojo": {"nojo", "repulsa"},
    "surpresa": {"surpreendido", "surpresa"}
}


def _token_stream(doc):
    for token in doc:
        yield token.text.lower(), token.lemma_.lower() if token.lemma_ else token.text.lower(), token.is_punct


def analyze_sentiment(doc) -> Dict[str, str]:
    """
    Analisa sentimento simples baseado em léxico e regras:
    - Polaridade: positivo/negativo/neutro
    - Emoção de texto: alegria/tristeza/raiva/medo/nojo/surpresa/neutro
    Considera negações locais (janela curta), intensificadores e pistas lexicais.
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
            token_score *= -1.0
            negate_window -= 1

        # Aplicar intensificador
        if token_score != 0.0:
            token_score *= intensifier
            # Depois de aplicar, regressar o intensificador ao normal
            intensifier = 1.0

        score += token_score

        # Contar pistas de emoção
        for emo, hints in EMOTION_HINTS.items():
            if text in hints or lemma in hints:
                emotion_counts[emo] += 1

    # Determinar polaridade
    if score > 0.25:
        polaridade = "positivo"
    elif score < -0.25:
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


if __name__ == "__main__":
    # Test
    doc = parse("Felizmente não chumbaram todos os alunos")
    print(analyze_sentiment(doc))
