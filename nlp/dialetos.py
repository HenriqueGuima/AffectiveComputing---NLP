import re

DIALETOS = {
    "NORTE": [
        "baca", "binho", "bassoura", "sapatilhas", "fino", "sertã", "tacho",
        "laurear a pevide", "briol", "dia de pico boi", "foguete nas meias", "patavina",
        "arreganhar a taxa", "esbardalhar", "aloquete", "alapar", "bitaites", "amarfanhar",
        "vergar a mola", "dar de frosques", "bicha", "estar com o toco", "breca", "jeco",
        "carago", "adiantar um grosso", "andar de cu tremido", "bolinha pinchona",
        "lapada", "chamar o gregorio", "comer o caco", "lampeira", "vai no batalha",
        "armar ao pingarelho", "vai me a loja", "broeiro", "acordar de cu pro ar",
        "arrotar postas de pescada", "andor violeta", "estrugido", "encher a mula"
        , "surbia", "molete", "ir de vela", "esticou o pernil",
        "bater a cacoleta", "foi fazer tijolos"
    ],
    "CENTRO": [
        "imperial", "sertã", "cruzeta", "testo", "jaco", "langao", "lafogao",
        "cachopo", "cachopa", "gazeteiro", "chafariz", "alpendre", "quebra",
        "quebrada", "quelha", "rilhada", "sobrado", "sopapada", "tonho",
        "tortulho", "vintaneira", "filho da parva do tovinho", "chatear o camoes",
        "encher a mula", "surbia", "molete", "fixe", "bue"
    ],
    "SUL": [
        "marafado", "bianda", "moce", "atarracar", "abicar", "serta", "serreiro",
        "marafado", "marafada", "sostra", "cua", "quina", "quelha", "quebra",
        "pexum", "cansum", "sovacum", "bedum", "ma que jete", "bem que me",
        "imperial", "refogado", "frigideira", "canito", "gateco"
    ],
    "MADEIRA": [
        "semilha", "semelha", "balcão", "bujarda", "ventoinha", "vizinhança",
        "adufa", "alcepas", "chavelha", "xavelha", "tratuario", "tenerifa",
        "afenafe", "semilha", "alendros", "alhendros", "alindres", "massapez",
        "borracheiro", "gamesse", "aboseirar", "bilhardeira", "buzico", "chimeco",
        "chorrica", "cigarrinho", "mamulhao", "mamulho", "modilho", "noveiro",
        "rebendita", "rijeiras", "roeza", "apilhagem"
    ],
    "ACORES": [
        "quarteirão", "alagoa", "amanhar", "galheta", "beberes", "alvaros",
        "alvarozes", "clauseta", "gama", "suera", "froca", "calafona", "briança",
        "destarelado", "enticar", "intenicar", "estapagado", "fominha negra",
        "gaitada", "gaitadaria", "maroiço", "marrolho", "tarelo", "rebendita",
        "besuga", "enxareu", "gueixo", "lapujo", "musgao", "piteiro", "bagoucho",
        "belica", "bailinho", "rapexim"
    ]
}

REGRAS_CONTEXTO = {
    "fino": [r"mais fino", r"muito fino", r"tão fino", r"extremamente fino", r"esta fino", r"mesmo fino"],
    "bicha": [r"bicha do cabelo", r"bicha de água", r"bicha de luz"],
    "patavina": [r"não percebo patavina", r"nem patavina"],
    "sertã": [r"cidade de sertã", r"vila de sertã", r"em sertã"],
    "imperial": [r"hotel imperial", r"palácio imperial", r"estilo imperial", r"império", r"imperialismo"],
    "sobrado": [r"sobrado de madeira", r"sobrado técnico"],
    "refogado": [r"base de refogado", r"refogado clássico", r"refogado tradicional"],
    "balcão": [r"balcão de atendimento", r"balcão de cozinha", r"balcão comercial"],
    "borracheiro": [r"oficina", r"pneu", r"automóvel"],
    "amanhar": [r"amanhar peixe", r"amanhar carne"],
    "gama": [r"gama de produtos", r"alta gama"],
}


def identificar_dialeto(frase):
    texto_input = str(frase).lower().strip()
    texto_processado = re.sub(r'[^\w\s]', '', texto_input)
    
    scores = {regiao: 0 for regiao in DIALETOS.keys()}

    for regiao, termos in DIALETOS.items():
        for termo in set(termos):
            t_busca = termo.lower().strip()
            pattern = r'\b' + re.escape(t_busca) + r'\b'
            
            if re.search(pattern, texto_processado):
                is_contexto_errado = False
                if t_busca in REGRAS_CONTEXTO:
                    for excecao in REGRAS_CONTEXTO[t_busca]:
                        if re.search(excecao, texto_processado):
                            is_contexto_errado = True
                            break
                
                if not is_contexto_errado:
                    scores[regiao] += 1  
    
    regioes_ordenadas = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    vencedor, pontuacao = regioes_ordenadas[0]
    
    if pontuacao == 0:
        return "PADRÃO"

    return vencedor