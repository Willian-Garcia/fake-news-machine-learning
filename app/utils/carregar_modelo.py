import joblib
from transformers import DistilBertTokenizer, DistilBertModel
import torch

def carregar_modelo():
    modelo = joblib.load("app/models/models_trained/modelo_treinado.pkl")
    label_encoder = joblib.load("app/models/models_trained/label_encoder.pkl")
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")
    bert_model.eval()
    return modelo, tokenizer, label_encoder, bert_model
