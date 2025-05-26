import spacy
import subprocess
import sys

print("Iniciando download do modelo spaCy para português...")
subprocess.check_call([sys.executable, "-m", "spacy", "download", "pt_core_news_sm"])
print("Modelo instalado com sucesso!") 