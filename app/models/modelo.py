from lime.lime_text import LimeTextExplainer
import numpy as np
import torch
from transformers import DistilBertTokenizer, DistilBertModel

def explicar_classificacao(texto, modelo_pipeline):
    tokenizer, bert_model, classificador = modelo_pipeline
    explainer = LimeTextExplainer(class_names=["falsa", "verdadeira"])

    def predict_proba(texts):
        embeddings = []
        for t in texts:
            inputs = tokenizer(t, return_tensors="pt", truncation=True, padding=True, max_length=512)
            inputs = {k: v.to(bert_model.device) for k, v in inputs.items()}
            with torch.no_grad():
                outputs = bert_model(**inputs)
            emb = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
            embeddings.append(emb)
        embeddings = np.array(embeddings)
        return classificador.predict_proba(embeddings)

    try:
        exp = explainer.explain_instance(texto, predict_proba, num_features=3)
        palavras = [w for w, _ in exp.as_list()]
        return palavras
    except Exception as e:
        print(f"Erro ao gerar explicação com LIME: {e}")
        return []
