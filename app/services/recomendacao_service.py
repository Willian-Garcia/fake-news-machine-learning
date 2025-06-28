import random
import pandas as pd
import os
import torch
from transformers import DistilBertTokenizer, DistilBertModel
from app.utils.carregar_modelo import carregar_modelo
from app.models.modelo import explicar_classificacao
from nltk.tokenize import sent_tokenize

# Verifica se há GPU disponível
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ⚠️ ORDEM IMPORTANTE: modelo, tokenizer, label_encoder, bert_model
modelo, tokenizer, label_encoder, bert_model = carregar_modelo()
bert_model.to(device)

# Diretórios de dados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Histórico de classificações
historico_resultados = []

def preprocessar_texto(texto: str) -> str:
    """Seleciona até as 5 primeiras frases do texto para reduzir custo computacional."""
    frases = sent_tokenize(texto)
    return " ".join(frases[:5])

def gerar_embedding(texto: str):
    """Gera o embedding do texto usando DistilBERT."""
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = bert_model(**inputs)
    embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
    return embedding.reshape(1, -1)

def classificar_texto(texto: str):
    """Classifica o texto como verdadeiro ou falso e retorna explicação."""
    if modelo is None or tokenizer is None or bert_model is None:
        raise Exception("Modelo, tokenizer ou BERT não carregado.")

    texto_preprocessado = preprocessar_texto(texto)
    embedding = gerar_embedding(texto_preprocessado)

    prob = modelo.predict_proba(embedding)[0]
    classe = modelo.predict(embedding)[0]
    classe_str = label_encoder.inverse_transform([classe])[0]
    probabilidade = max(prob)

    palavras = explicar_classificacao(texto, modelo_pipeline=(tokenizer, bert_model, modelo))

    resultado = {
        "classe": classe_str,
        "probabilidade": round(probabilidade, 2),
        "palavras_influentes": palavras
    }

    historico_resultados.append(resultado)
    return resultado

def pegar_exemplo(retornar_rotulo=False):
    """Seleciona aleatoriamente uma notícia do dataset."""
    tipo = random.choice(["Fake", "True"])
    path = os.path.join(DATA_DIR, f"{tipo}.csv")

    if not os.path.isfile(path):
        raise FileNotFoundError(f"⚠️ Arquivo não encontrado: {path}")

    df = pd.read_csv(path)
    index = random.randint(0, len(df) - 1)
    linha = df.iloc[index]
    texto = f"{linha['title']} {linha['text']}".strip()
    origem = f"{path} (linha {index})"

    if retornar_rotulo:
        rotulo = "falsa" if tipo == "Fake" else "verdadeira"
        return texto, origem, rotulo
    return texto, origem

def obter_historico():
    """Retorna histórico de classificações realizadas."""
    return historico_resultados

def status_modelo():
    """Indica se o modelo está carregado corretamente."""
    return {"modelo_carregado": modelo is not None}
