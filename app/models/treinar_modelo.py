import os
import pandas as pd
import torch
import joblib
import numpy as np
from tqdm import tqdm
from transformers import DistilBertTokenizer, DistilBertModel
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import nltk

nltk.download("punkt")

# Caminhos
DATA_DIR = "../data"
SAVE_DIR = "./models_trained"
os.makedirs(SAVE_DIR, exist_ok=True)

# 1. Carregar dados
fake = pd.read_csv(os.path.join(DATA_DIR, "Fake.csv"))
true = pd.read_csv(os.path.join(DATA_DIR, "True.csv"))
fake["label"] = "falsa"
true["label"] = "verdadeira"

df = pd.concat([fake, true])[['title', 'text', 'label']].dropna()
df['texto'] = df['title'] + ' ' + df['text']

# 2. Amostragem balanceada com limite de 1000 por classe
limite = 1000
df_bal = df.groupby('label').apply(lambda x: x.sample(min(len(x), limite), random_state=42)).reset_index(drop=True)
print(f"📊 Dados balanceados (amostrados): {df_bal['label'].value_counts().to_dict()}")

# 3. Codificar labels
y = LabelEncoder()
y_labels = y.fit_transform(df_bal['label'])

# 4. Tokenizer + DistilBERT
print("📦 Carregando tokenizer e modelo DistilBERT...")
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
bert.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert.to(device)

# 5. Função para gerar embeddings
@torch.no_grad()
def gerar_embedding_batch(batch_texts):
    inputs = tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    outputs = bert(**inputs)
    return outputs.last_hidden_state[:, 0, :].cpu().numpy()

# 6. Gerar todos os embeddings
print("🧠 Gerando embeddings com DistilBERT...")
conteudos = df_bal['texto'].tolist()
batch_size = 32
embeddings = []

for i in tqdm(range(0, len(conteudos), batch_size)):
    batch = conteudos[i:i+batch_size]
    emb = gerar_embedding_batch(batch)
    embeddings.append(emb)

X = np.vstack(embeddings)

# 7. Treinar modelo
print("⚙️ Treinando modelo de classificação...")
X_train, X_test, y_train, y_test = train_test_split(X, y_labels, test_size=0.2, random_state=42)
modelo = LogisticRegression(max_iter=1000, class_weight="balanced")
modelo.fit(X_train, y_train)

# 8. Avaliação
y_pred = modelo.predict(X_test)
print("\n✅ Avaliação do Modelo:")
print(classification_report(y_test, y_pred, target_names=y.classes_))
print("Acurácia:", round(accuracy_score(y_test, y_pred), 4))

# 9. Salvar tudo
joblib.dump(modelo, os.path.join(SAVE_DIR, "modelo_treinado.pkl"))
joblib.dump(y, os.path.join(SAVE_DIR, "label_encoder.pkl"))
print("💾 Modelo e encoder salvos com sucesso!")
