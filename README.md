# HotelEvaluator

Analisador de comentários de hóspedes para hotéis com processamento de linguagem natural em português.

## Sobre o projeto

Este projeto utiliza técnicas de processamento de linguagem natural (NLP) para analisar comentários de clientes de hotéis em português. A aplicação identifica:

- Sentimento (positivo, negativo ou neutro)
- Aspectos específicos do hotel mencionados (quarto, comida, atendimento, etc.)
- Sugestões de melhoria baseadas na análise

## Tecnologias

- **Backend**: Python com Flask
- **NLP**: Biblioteca spaCy com modelo em português
- **Frontend**: HTML, CSS (Tailwind) e JavaScript

## Como rodar localmente

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Baixe o modelo spaCy em português: `python -m spacy download pt_core_news_sm`
4. Execute a aplicação: `python main.py`
5. Acesse http://localhost:5000 no navegador

## Hospedagem

Este projeto está hospedado via Render <a>https://hotel-evaluator.onrender.com/</a>
