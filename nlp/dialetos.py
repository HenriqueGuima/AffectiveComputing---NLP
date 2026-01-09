import re

DIALETOS = {
    "NORTE": {
        "baca": "vaca", "binho": "vinho", "bassoura": "vassoura", "beber": "beber",
        "sapatilhas": "ténis", 
        "fino": "imperial", 
        "sertã": "frigideira",
        "tacho": "panela",
        # Dia a dia e Objetos
        "laurear a pevide": "passear",
        "briol": "frio",
        "dia de pico boi": "dia de trabalho",
        "foguete nas meias": "buraco nas meias",
        "patavina": "nada",
        "arreganhar a taxa": "rir",
        "esbardalhar": "cair",
        "aloquete": "cadeado",
        "alapar": "sentar",
        "bitaites": "palpites",
        "amarfanhar": "espremer",
        "vergar a mola": "trabalhar muito",
        "dar de frosques": "ir embora",
        "bicha": "fila",
        "estar com o toco": "mal-humorado",
        "breca": "cãibra",
        "jeco": "cão",
        "carago": "interjeição",
        "adiantar um grosso": "inútil",
        "andar de cu tremido": "andar de carro",
        "bolinha pinchona": "bolinha saltitona",
        "lapada": "estalo",
        "chamar o gregorio": "vomitar",
        "comer o caco": "confundir",

        # 'Insultos' e 'Bocas' (Deteção de tom)
        "lampeira": "vaidosa",
        "vai no batalha": "mentira",
        "armar ao pingarelho": "exibir-se",
        "vai me a loja": "nao me chateies",
        "broeiro": "rude",
        "acordar de cu pro ar": "mal-disposto",
        "arrotar postas de pescada": "gabar-se",
        "andor violeta": "vai-te embora",

        # Comer e Beber
        "estrugido": "refogado",
        "encher a mula": "comer muito",
        "fino": "imperial",
        "pneu": "agua das pedras com limao",
        "surbia": "cerveja",
        "molete": "pao",

        # Morte (ou fim de algo)
        "ir de vela": "acabou",
        "esticou o pernil": "morreu",
        "bater a cacoleta": "morreu",
        "foi fazer tijolos": "morreu"
        
    },
    "CENTRO": {
        "imperial": "fino",
        "sertã": "frigideira",
        "cruzeta": "cabide",
        "testo": "tampa",
        # Vocabulário Específico
        "jaco": "caixote do lixo",
        "langao": "preguiçoso",
        "lafogao": "comilão",
        "cachopo": "rapaz",
        "cachopa": "rapariga",
        "gazeteiro": "falta as aulas",
        "chafariz": "fonte",
        "alpendre": "varanda",
        
        # Beira Interior
        "quebra": "falir",
        "quebrada": "encosta",
        "quelha": "viela",
        "rilhada": "jogo local",
        "sobrado": "sotao",
        "sopapada": "bofetada",
        "tonho": "vadio",
        "tortulho": "desajeitado",
        "vintaneira": "vento",

        # Expressões e Frases
        "filho da parva do tovinho": "expressao de desaprovacao",
        "chatear o camoes": "incomodar",
        "encher a mula": "comer muito",
        "fino": "imperial",
        "pneu": "agua das pedras com limao",
        "surbia": "cerveja",
        "molete": "pao",
        
        # Marcadores de intensidade (Úteis para o NLP entender o sentimento)
        "fixe": "bom",
        "bue": "muito"
    },
    "SUL": {
        "marafado": "irritado",
        "bianda": "comida",
        "moce": "rapaz",
        "atarracar": "apertar",
        "abicar": "aproximar",
        # Vocabulário e Objetos
        "serta": "frigideira",
        "serreiro": "natural da serra",
        "marafado": "irritado ou trapaceiro",
        "marafada": "irritada ou trapaceira",
        "sostra": "preguiçoso",
        "cua": "gordo",
        "quina": "esquina",
        "quelha": "viela",
        "quebra": "falir",

        # Termos de Cheiro (O Vosk pode ter dificuldade aqui, são ótimos para o dicionário)
        "pexum": "cheiro a peixe",
        "cansum": "cheiro a cao",
        "sovacum": "cheiro a axila",
        "bedum": "mau cheiro",

        # Expressões de Intensidade/Espanto
        "ma que jete": "que espanto",
        "bem que me": "expressao de intensidade",
        
        # Bebidas e Comida (O contraste clássico)
        "imperial": "cerveja", # O marcador definitivo do Sul
        "refogado": "estrugido",
        "frigideira": "serta",

        # Diminutivos (Para o teu NLP ignorar o sufixo e focar no radical)
        "canito": "cao",
        "gateco": "gato"
    },
    "MADEIRA": {
        "semilha": "batata",
        "semelha": "batata",
        "balcão": "esplanada",
        "bujarda": "mentira",
        "ventoinha": "ventilador",
        "vizinhança": "vizinhos",
        # Objetos e Casa
        "adufa": "janela ou portinhola",
        "alcepas": "alicerce",
        "chavelha": "peça de carro de bois / pessoa teimosa",
        "xavelha": "peça de carro de bois",
        "tratuario": "passeio", # O Vosk vai ouvir 'tratuário' e não 'trotuário'
        "tenerifa": "renda tipica",
        "afenafe": "rapidez ou energia",

        # Comida e Natureza
        "semilha": "batata", # O marcador mais importante da Madeira
        "alendros": "tremoços",
        "alhendros": "tremoços",
        "alindres": "tremoços",
        "massapez": "terreno argiloso",
        "borracheiro": "fabricante de odres / planta",
        "gamesse": "tipo de planta/erva",

        # Pessoas e Comportamentos
        "aboseirar": "sentar ou descansar",
        "bilhardeira": "fofoqueira",
        "buzico": "criança pequena",
        "chimeco": "pessoa de baixa estatura",
        "chorrica": "pessoa fraca ou chorona",
        "cigarrinho": "pessoa magra ou cigarro pequeno",
        "mamulhao": "grande quantidade ou amontoado",
        "mamulho": "amontoado",
        "modilho": "maneira ou feitio",
        "noveiro": "pessoa que faz intrigas",
        "rebendita": "teimosia ou picardia",
        "rijeiras": "força ou resistencia",
        "roeza": "vontade de comer ou roer",
        
        # Diversos
        "apilhagem": "ajuntamento ou pilha"
    },
    "ACORES": {
        "quarteirão": "bloco de casas",
        "alagoa": "lagoa",
        "amanhar": "preparar",
        "galheta": "estalo",
        "beberes": "bebidas",
        # Influência do Inglês (Crucial para o Vosk não baralhar)
        "alvaros": "macacao", # De 'overall'
        "alvarozes": "macacao",
        "clauseta": "armario", # De 'closet'
        "gama": "pastilha elastica", # De 'gum'
        "suera": "camisola", # De 'sweater'
        "froca": "casaco", # De 'frock coat'
        "calafona": "California", # Referência ao estado americano

        # Vocabulário Local e Expressões
        "briança": "criança", # Variação fonética comum
        "destarelado": "pessoa que fala muito / tonto",
        "enticar": "implicar",
        "intenicar": "implicar / provocar",
        "estapagado": "parvo / tonto",
        "fominha negra": "fome extrema",
        "gaitada": "risada",
        "gaitadaria": "muitas risadas",
        "maroiço": "monte de pedras",
        "marrolho": "mar agitado",
        "tarelo": "juízo / conversa",
        "rebendita": "vingança / teimosia",
        
        # Animais e Natureza
        "besuga": "besugo (peixe)",
        "enxareu": "peixe enxareu",
        "gueixo": "bezerro / vitelo",
        "lapujo": "sujidade de lapa",
        "musgao": "musgo grande",
        "piteiro": "tipo de planta / agave",
        
        # Outros
        "bagoucho": "pedaço pequeno",
        "belica": "pequena porção de algo",
        "bailinho": "dança típica",
        "rapexim": "natural de Rabo de Peixe"
    }
}

def identificar_dialeto(frase):
    texto_input = str(frase).lower().strip()
    
    texto_input = re.sub(r'[^\w\s]', '', texto_input)
    
    print(f"\n--- DEBUG DIALETO ---")
    print(f"Frase processada: '{texto_input}'")

    scores = {regiao: 0 for regiao in DIALETOS.keys()}

    for regiao, termos in DIALETOS.items():
        for termo in termos.keys():
            t_busca = termo.lower().strip()
            if t_busca in texto_input:
                pattern = r'\b' + re.escape(t_busca) + r'\b'
                if re.search(pattern, texto_input):
                    scores[regiao] += 1
                    print(f"MATCH: '{termo}' encontrado em {regiao}")

    print(f"Pontuação final: {scores}")
    
    regiao_vencedora = max(scores, key=scores.get)
    if scores[regiao_vencedora] == 0:
        return "PADRÃO"

    return regiao_vencedora