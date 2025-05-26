#!/bin/bash
pip install -r requirements.txt
python -m spacy download pt_core_news_sm
python download_models.py 