import random
import pandas as pd
import os
import torch
import nltk
from transformers import DistilBertTokenizer, DistilBertModel
from app.utils.carregar_modelo import carregar_modelo
# from app.models.modelo import explicar_classificacao  # Comentado
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("punkt")

punkt_params = PunktParameters()
tokenizer_sentencas = PunktSentenceTokenizer(punkt_params)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

modelo, tokenizer, label_encoder, bert_model = carregar_modelo()
bert_model.to(device)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

historico_resultados = []

# Inicializa vetor para TF-IDF
corpus_tfidf = []

# Carrega corpus para treinar TF-IDF
try:
    df_fake = pd.read_csv(os.path.join(DATA_DIR, "Fake.csv"))
    df_true = pd.read_csv(os.path.join(DATA_DIR, "True.csv"))
    corpus_tfidf = pd.concat([df_fake, df_true])["text"].fillna("").tolist()
    tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    tfidf_vectorizer.fit(corpus_tfidf)
except Exception as e:
    print(f"⚠️ Erro ao treinar TF-IDF: {e}")
    tfidf_vectorizer = None


def explicar_por_tfidf(texto: str, top_n: int = 5):
    if not tfidf_vectorizer:
        return []
    vetor = tfidf_vectorizer.transform([texto])
    indices = vetor.nonzero()[1]
    pesos = vetor.data
    palavras = [tfidf_vectorizer.get_feature_names_out()[i] for i in indices]
    ordenadas = sorted(zip(palavras, pesos), key=lambda x: x[1], reverse=True)
    return [p for p, _ in ordenadas[:top_n]]


def preprocessar_texto(texto: str) -> str:
    frases = tokenizer_sentencas.tokenize(texto)
    return " ".join(frases[:5])


def gerar_embedding(texto: str):
    inputs = tokenizer(texto, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = bert_model(**inputs)
    embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
    return embedding.reshape(1, -1)


def classificar_texto(texto: str):
    if modelo is None or tokenizer is None or bert_model is None:
        raise Exception("Modelo, tokenizer ou BERT não carregado.")

    texto_preprocessado = preprocessar_texto(texto)
    embedding = gerar_embedding(texto_preprocessado)

    prob = modelo.predict_proba(embedding)[0]
    classe = modelo.predict(embedding)[0]
    classe_str = label_encoder.inverse_transform([classe])[0]
    probabilidade = max(prob)

    # Tentativa de usar explicação com SHAP
    try:
        # palavras = explicar_classificacao(texto, modelo_pipeline=(tokenizer, bert_model, modelo))  # método lento
        raise NotImplementedError  # força uso do TF-IDF neste exemplo
    except Exception:
        palavras = explicar_por_tfidf(texto)

    resultado = {
        "classe": classe_str,
        "probabilidade": round(probabilidade, 2),
        "palavras_influentes": palavras,
    }

    historico_resultados.append(resultado)
    return resultado


def pegar_exemplo(retornar_rotulo=False):
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
    return historico_resultados


def status_modelo():
    return {"modelo_carregado": modelo is not None}
