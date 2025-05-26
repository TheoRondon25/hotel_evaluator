from numpy import positive
import spacy;
import unicodedata;
import re;
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass

#Carrega o modelo de linguagem em português do spacy
nlp = spacy.load("pt_core_news_sm");

# Função para gerar automaticamente formas masculinas, femininas, singulares e plurais
def expandir_genero(palavras: List[str]) -> Set[str]:
    """
    Gera automaticamente as formas masculinas, femininas, singulares e plurais das palavras
    baseadas em regras simples de português.
    
    Args:
        palavras: Lista de palavras a serem expandidas
        
    Returns:
        Conjunto com todas as palavras originais e suas variações de gênero
    """
    resultado = set()
    
    for palavra in palavras:
        # Adiciona a palavra original
        resultado.add(palavra)
        
        # Regras comuns de conversão português
        if palavra.endswith('o'):  # masculino -> feminino (ex: bonito -> bonita)
            resultado.add(palavra[:-1] + 'a')
            resultado.add(palavra + 's')  # plural masculino
            resultado.add(palavra[:-1] + 'as')  # plural feminino
        elif palavra.endswith('a'):  # feminino -> masculino (ex: bonita -> bonito)
            resultado.add(palavra[:-1] + 'o')
            resultado.add(palavra + 's')  # plural feminino
            resultado.add(palavra[:-1] + 'os')  # plural masculino
        elif palavra.endswith('os'):
            resultado.add(palavra[:-2] + 'o')
            resultado.add(palavra[:-2] + 'a')
            resultado.add(palavra[:-2] + 'as')
        elif palavra.endswith('as'):
            resultado.add(palavra[:-2] + 'a')
            resultado.add(palavra[:-2] + 'o')
            resultado.add(palavra[:-2] + 'os')
        elif palavra.endswith('or'):  # (ex: encantador -> encantadora)
            resultado.add(palavra + 'a')
            resultado.add(palavra + 'es')
            resultado.add(palavra + 'as')
        else:
            # Adiciona plural simples
            resultado.add(palavra + 's')
        
    return resultado

# Definições base de palavras
positivas_base = ["otimo", "excelente", "perfeito", "maravilhoso", "agradavel", 
                 "bom", "incrivel", "fantastico", "delicioso", "espetacular", 
                 "surpreendente", "esplendido", "encantador", "satisfatorio"]
                 
negativas_base = ["pessimo", "ruim", "terrivel", "desagradavel", "horrivel", 
                 "fraco", "insatisfatorio", "inadequado", "decepcionante", 
                 "desapontador", "deploravel", "lamentavel"]
                 
neutras_base = ["normal", "razoavel", "ok", "regular", "medio", "comum", "aceitavel"]

areas_base = ["quarto", "estadia", "comida", "restaurante", "atendimento", "piscina", 
            "area", "infantil", "de", "lazer", "academia", "limpeza", "localizacao", 
            "hotel", "cafe", "servico", "servicos", "funcionarios", "vista", "preco"]

# Define as categorias da gramática e os respectivos conjuntos(tokens) de palavras associadas a cada categoria
tokens_gramatica = {
    "Det": {"o", "a", "essa", "esse", "minha", "meu"},
    "Verb": {"foi", "esta", "é", "parece", "sao", "estao", "estava", "estar", "ser"},
    "Intensificador": {"muito", "super", "pouco", "bastante", "extremamente"},
    "Positivo": expandir_genero(positivas_base),
    "Negativo": expandir_genero(negativas_base),
    "Neutro": expandir_genero(neutras_base),
    "Area": set(areas_base),
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

def validar_texto(texto: str) -> bool:
    """
    Valida se o texto contém pelo menos uma palavra de cada categoria necessária.
    
    Args:
        texto (str): O texto a ser validado
        
    Returns:
        bool: True se o texto contém palavras válidas, False caso contrário
    """
    # Converte para minúsculo e remove pontuação
    texto = texto.lower()
    texto = texto.replace('.', '').replace(',', '')
    
    # Divide em palavras e remove acentos, exceto do verbo "é"
    palavras = []
    for palavra in texto.split():
        if palavra == "é":
            palavras.append(palavra)
        else:
            palavras.append(remover_acentos(palavra))
    
    # Verifica se tem pelo menos uma palavra de cada categoria
    tem_area = any(
        palavra in tokens_gramatica["Area"] or 
        remover_acentos(palavra) in tokens_gramatica["Area"] 
        for palavra in palavras
    )
    
    tem_verbo = any(
        palavra in tokens_gramatica["Verb"] or 
        remover_acentos(palavra) in tokens_gramatica["Verb"] 
        for palavra in palavras
    )
    
    tem_intensificador = any(
        palavra in tokens_gramatica["Intensificador"] or 
        remover_acentos(palavra) in tokens_gramatica["Intensificador"] 
        for palavra in palavras
    )
    
    # Verifica se tem pelo menos uma palavra de sentimento (positivo, negativo ou neutro)
    tem_sentimento = any(
        palavra in tokens_gramatica["Positivo"] or
        palavra in tokens_gramatica["Negativo"] or
        palavra in tokens_gramatica["Neutro"] or
        remover_acentos(palavra) in tokens_gramatica["Positivo"] or
        remover_acentos(palavra) in tokens_gramatica["Negativo"] or
        remover_acentos(palavra) in tokens_gramatica["Neutro"]
        for palavra in palavras
    )
    
    # Debug: imprime as palavras encontradas
    print(f"Palavras limpas: {palavras}")
    print(f"Tem área: {tem_area}")
    print(f"Tem verbo: {tem_verbo}")
    print(f"Tem intensificador: {tem_intensificador}")
    print(f"Tem sentimento: {tem_sentimento}")
    
    # Retorna True se tiver pelo menos uma palavra de cada categoria necessária
    return tem_area and (tem_verbo or tem_intensificador) and tem_sentimento

@dataclass
class EvaluationResult:
    aspect: str
    sentiment: str
    intensifier: Optional[str] = None


class HotelEvaluator:
    def __init__(self):
        self.nlp = spacy.load("pt_core_news_sm")

    def evaluate_comment(self, comment: str) -> dict:
        """
        Avalia um comentário sobre um hotel e retorna uma análise de sentimento.
        
        Args:
            comment (str): O comentário a ser avaliado
            
        Returns:
            dict: Dicionário contendo a qualidade geral e os aspectos avaliados
        """
        if not comment or not isinstance(comment, str):
            return {"error": "Comentário inválido"}
            
        # Valida se o texto contém palavras válidas
        if not validar_texto(comment):
            return {"error": "O texto não contém palavras válidas para avaliação. Use palavras relacionadas a áreas do hotel (quarto, comida, serviço), verbos (é, foi, estava) e adjetivos (ótimo, ruim, bom)."}

        # Processa o comentário
        doc = self.nlp(comment.lower())
        
        # Inicializa variáveis para análise
        current_aspect = None
        current_intensifier = None
        results = []
        sentiments = []
        negacao = False
        
        # Analisa cada token
        for token in doc:
            token_text = token.text.lower()
            token_text_sem_acento = remover_acentos(token_text)
            token_lemma = remover_acentos(token.lemma_.lower())

            # Verifica negação
            if token_text == 'não' or token_text_sem_acento == 'nao':
                negacao = True
                continue
            
            # Verifica se é um aspecto
            if (token_text in tokens_gramatica["Area"] or 
                token_text_sem_acento in tokens_gramatica["Area"] or
                token_lemma in tokens_gramatica["Area"]):
                current_aspect = token_text
            
            # Verifica se é um intensificador
            elif (token_text in tokens_gramatica["Intensificador"] or 
                  token_text_sem_acento in tokens_gramatica["Intensificador"] or
                  token_lemma in tokens_gramatica["Intensificador"]):
                current_intensifier = token_text
            
            # Verifica se é um sentimento
            elif (token_text in tokens_gramatica["Positivo"] or 
                  token_text_sem_acento in tokens_gramatica["Positivo"] or
                  token_lemma in tokens_gramatica["Positivo"]):
                sentiment = "negativo" if negacao else "positivo"
                results.append({
                    "aspect": current_aspect or "geral",
                    "sentiment": sentiment,
                    "intensifier": current_intensifier
                })
                sentiments.append(-1 if negacao else 1)
                current_intensifier = None
                negacao = False
                
            elif (token_text in tokens_gramatica["Negativo"] or 
                  token_text_sem_acento in tokens_gramatica["Negativo"] or
                  token_lemma in tokens_gramatica["Negativo"]):
                sentiment = "positivo" if negacao else "negativo"
                results.append({
                    "aspect": current_aspect or "geral",
                    "sentiment": sentiment,
                    "intensifier": current_intensifier
                })
                sentiments.append(1 if negacao else -1)
                current_intensifier = None
                negacao = False
                
            elif (token_text in tokens_gramatica["Neutro"] or 
                  token_text_sem_acento in tokens_gramatica["Neutro"] or
                  token_lemma in tokens_gramatica["Neutro"]):
                sentiment = "neutro"
                results.append({
                    "aspect": current_aspect or "geral",
                    "sentiment": sentiment,
                    "intensifier": current_intensifier
                })
                sentiments.append(0)
                current_intensifier = None
                negacao = False
        
        # Determina a qualidade geral com base nos sentimentos encontrados
        if not sentiments:
            overall_quality = "neutro"
        else:
            avg_sentiment = sum(sentiments) / len(sentiments)
            if avg_sentiment > 0.3:
                overall_quality = "positivo"
            elif avg_sentiment < -0.3:
                overall_quality = "negativo"
            else:
                overall_quality = "neutro"
        
        return {
            "quality": overall_quality,
            "results": results
        }

    def parse_comment(self, comment: str) -> dict:
        tokens = categorizar_tokens(comment)
        if any(cat == "Desconhecido" for _, cat in tokens):
            return {"error": "Comentário inválido conforme a gramática fornecida"}
        
        results = []
        current_aspect = []
        current_verb = None
        current_intesifier = None
        current_eval = None
        
        i = 0
        
        while i < len(tokens):
            token, cat = tokens[i]
            if cat== "Det":
                i+=1
                continue
            if cat == "Area":
                current_aspect.append(token)
                # Verifica se o próximo token forma um aspecto composto (ex.: "area de lazer")
                if i + 2 < len(tokens) and tokens[i+1][0] == "de" and tokens[i+2] =="Area":
                    current_aspect.extend([tokens[i + 1][0], tokens[i+2][0]])
                    i += 3
                else:
                    i += 1
                    continue
            if cat=="Verb":
                current_verb = token
                i += 1
                continue
            if cat=="Intensificador":
                current_intesifier = token
                i += 1
                continue
            if cat==["Positivo","Negativo","Neutro"]:
                current_eval = token
                if current_aspect and current_verb and current_eval:
                    aspect = "".join(current_aspect)
                    sentiment = "positivo" if cat == "Positivo" else "negativo" if cat == "Negativo" else "neutro"
                    results.append({
                        "aspect":aspect,
                        "sentiment": sentiment,
                        "intensifier": current_intesifier
                    })
                    current_aspect=[]
                    current_verb = current_intesifier = current_eval = None
                i += 1
                continue
            if cat=="Conector":
                current_aspect = []
                current_verb = current_intesifier = current_eval = None
                i += 1
                continue
            i+=1 
            
            
            if not results:
                return {"error": "Nenhum aspecto válido identificado"}
            
            positive_count = sum(1 for r in results if r["sentiment"] == "positivo")
            negative_count = sum(1 for r in results if r["sentiment"] == "negativo")
            neutral_count = sum(1 for r in results if r["sentiment"] == "neutro")
            
            if negative_count > 0:
                quality = "ruim"
            elif positive_count == len(results):
                quality = "excelente"
            else:
                quality = "bom"
            
            return {
                "results": results,
                "quality": quality
            }
                    