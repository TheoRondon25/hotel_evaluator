# HotelEvaluator 🏨🔍

![HotelEvaluator Screenshot](./images/pagina%20inicial.png)

Analisador de comentários de hóspedes para hotéis com **Processamento de Linguagem Natural (NLP)** em português.

## 🚀 Sobre o projeto

O **HotelEvaluator** utiliza técnicas de NLP para analisar comentários de clientes de hotéis em português. A aplicação identifica:

- **Sentimento** (positivo, negativo ou neutro)
- **Aspectos específicos** do hotel mencionados (quarto, comida, atendimento, etc.)
- **Sugestões de melhoria** baseadas na análise

## 🛠️ Tecnologias

- **Backend:** Python + Flask
- **NLP:** spaCy (modelo pt_core_news_sm)
- **Frontend:** HTML, CSS (Tailwind) e JavaScript

## ⚡ Como rodar localmente

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Baixe o modelo spaCy em português: `python -m spacy download pt_core_news_sm`
4. Execute a aplicação: `python main.py`
5. Acesse http://localhost:5000 no navegador

## Hospedagem

Este projeto está hospedado na plataforma Render <a>https://hotel-evaluator.onrender.com/</a>

Desenvolvido por [Kevin](https://www.linkedin.com/in/kevin-lopes-151797221/)
