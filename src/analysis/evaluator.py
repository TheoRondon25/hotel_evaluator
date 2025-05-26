import spacy;
import unicodedata;
import re;

#Carrega o modelo de linguagem em português do spacy
nlp = spacy.load("pt_core_news_sm");


# Define as categorias da gramática e os respectivos conjuntos(tokens) de palavras associadas a cada categoria
tokens_gramatica = {
    "Det": {"o", "a", "essa", "esse", "minha", "meu"},
    "Verb": {"foi", "esta", "é", "parece", "sao", "estao", "estava", "estar", "ser"},
    "Intensificador": {"muito", "super", "pouco", "bastante", "extremamente"},
    "Positivo": {"otimo", "otima", "excelente", "perfeito", "maravilhoso", "maravilhosa", "agradavel", "bom", "boa"},
    "Negativo": {"pessimo", "pessima", "ruim", "terrivel", "desagradavel", "horrivel"},
    "Neutro": {"normal", "razoavel", "ok", "regular"},
    "Area": {"quarto", "estadia", "comida", "restaurante", "atendimento", "piscina", "area", "infantil", "de", "lazer", "academia", "limpeza", "localizacao"},
    "Conector": {"mas", "porem", "e", "contudo", "entretanto", ","}
}

# Função que remove acentos e cedilhas de um texto (normalização para facilitar a comparação)
def remover_acentos(texto):
    texto = unicodedata.normalize('NFD', texto)
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = texto.replace('ç', 'c').replace('Ç', 'C')
    return texto

# Função que lemmatiza uma frase (transforma as palavras em suas formas base) e remove acentos
def lemmatizar_frase(frase):
    doc = nlp(frase)
    lemas = [remover_acentos(token.lemma_.lower()) for token in doc]
    originais = [token.text for token in doc]
    return list(zip(originais, lemas))

# Função que categoriza os tokens de uma frase
def categorizar_tokens(frase):
    frase = remover_acentos(frase.lower())
    tokens_lematizados = lemmatizar_frase(frase)
    resultado = []

    for original, lema in tokens_lematizados:
        categoria = None
        for cat, palavras_set in tokens_gramatica.items():
            if lema in palavras_set or original in palavras_set:
                categoria = cat
                break
        resultado.append((original, categoria or "Desconhecido"))
    return resultado


class HotelEvaluator:
    def evaluete_comment(self, comment:str) -> dict:
        tokens = categorizar_tokens(comment)
        if any (cat == "Desconhecido" for _, cat in tokens):
            return {"error":"Comentário inválido conforme a gramática fornecida"}