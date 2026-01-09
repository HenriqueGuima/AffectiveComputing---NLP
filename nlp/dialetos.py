import re

DIALETOS = {
    "NORTE": [
        "baca", "binho", "bassoura", "beber", "sapatilhas", "fino", "sertã", "tacho",
        "laurear a pevide", "briol", "dia de pico boi", "foguete nas meias", "patavina",
        "arreganhar a taxa", "esbardalhar", "aloquete", "alapar", "bitaites", "amarfanhar",
        "vergar a mola", "dar de frosques", "bicha", "estar com o toco", "breca", "jeco",
        "carago", "adiantar um grosso", "andar de cu tremido", "bolinha pinchona",
        "lapada", "chamar o gregorio", "comer o caco", "lampeira", "vai no batalha",
        "armar ao pingarelho", "vai me a loja", "broeiro", "acordar de cu pro ar",
        "arrotar postas de pescada", "andor violeta", "estrugido", "encher a mula",
        "fino", "pneu", "surbia", "molete", "ir de vela", "esticou o pernil",
        "bater a cacoleta", "foi fazer tijolos"
    ],
    "CENTRO": [
        "imperial", "sertã", "cruzeta", "testo", "jaco", "langao", "lafogao",
        "cachopo", "cachopa", "gazeteiro", "chafariz", "alpendre", "quebra",
        "quebrada", "quelha", "rilhada", "sobrado", "sopapada", "tonho",
        "tortulho", "vintaneira", "filho da parva do tovinho", "chatear o camoes",
        "encher a mula", "fino", "pneu", "surbia", "molete", "fixe", "bue"
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

def identificar_dialeto(frase):
    texto_input = str(frase).lower().strip()
    
    texto_input = re.sub(r'[^\w\s]', '', texto_input)
    
    print(f"\n--- DEBUG DIALETO ---")
    print(f"Frase processada: '{texto_input}'")

    scores = {regiao: 0 for regiao in DIALETOS.keys()}

    for regiao, termos in DIALETOS.items():
        for termo in termos:
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