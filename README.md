# 📰 API de Classificação de Notícias Falsas (Fake News)

Este projeto utiliza embeddings do **DistilBERT** combinados com um classificador **Logistic Regression** para detectar se uma notícia em inglês é **falsa** ou **verdadeira**. A API foi desenvolvida com **FastAPI**.

---

## 🚀 Funcionalidades

- 🔍 Classificação de notícias como **falsas** ou **verdadeiras**
- 🤖 Geração de embeddings com **DistilBERT**
- 📈 Retorno da probabilidade da classificação
- 💡 Suporte a explicações por palavras mais influentes (opcional, via LIME)
- 🧠 Histórico de classificações durante a sessão
- ⚡ API REST com **FastAPI**

> ⚠️ Os textos analisados devem estar em **inglês**

---

## 📁 Estrutura do Projeto

```
app/
├── main.py # Ponto de entrada da API
├── data/
│ └── Fake.csv # Dataset
│ └── True.csv # Dataset
├── routers/
│ └── recomendacoes.py # Rotas da API
├── services/
│ └── recomendacao_service.py # Lógica principal de classificação
├── models/
│ └── models_trained/ # Modelo e encoder salvos
│ └── modelo.py # Geração de explicações com LIME (opcional)
│ └── treinar_modelo.py # Script de treinamento
├── schemas/
│ └── recomendacao.py # Esquemas de entrada/saída da API (Pydantic)
├── utils/
│ └── carregar_modelo.py # Carregamento do modelo e tokenizer 
└── requirements.txt # Dependências do projeto
```

---

## ⚙️ Como rodar o projeto

## ⚙️ Configurando o Backend

### 1. Clone o repositório e crie o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
```

### 2. Instale as dependências

```bash
cd app
pip install -r requirements.txt
cd ..
```

### 3. Execute a API com Uvicorn

```bash
uvicorn app.main:app --reload
```

## ⚙️ Configurando o Frontend

### 1. Instalando Dependências

```bash
cd frontend
npm i
```

### 2. Execute o Frontend

```bash
npm start
```

### 4. Acesse a interface de testes (Swagger UI)

👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 Endpoints

### `POST /api/classificar-noticia`
Classifica um texto como **Fake** ou **True**.

**Body JSON:**
```json
{
  "texto": "President signs new climate agreement with international support.",
  "usar_exemplo": "false"
}
```

**Resposta:**
```json
{
  "classe": "verdadeira",
  "probabilidade": 0.98,
  "palavras_influentes": []
}
```

---

### `GET /api/historico`
Retorna o histórico de classificações realizadas.

### `GET /api/status`
Retorna status atual do modelo carregado (tipo, embeddings, versão).

---

## 🧠 Modelo

- **Embeddings:** `DistilBERT (distilbert-base-uncased)`
- **Classificador:** `LogisticRegression`
- **Explicações:** `LIME`
- **Dados:** Fake and Real News Dataset (Kaggle)

---

## 📝 Observações
- O uso de LIME para explicações pode deixar a resposta mais lenta.
- O desempenho do modelo depende da CPU/GPU disponível.
- Para produção, considere otimizar o pipeline (salvando embeddings ou usando modelos otimizados).

## 📄 Licença

Este projeto é de uso educacional e acadêmico. Para uso em produção, é importante aplicar filtros adicionais, controle de viés e validação contínua.

---

## 🙋‍♂️ Contato

Dúvidas ou sugestões? Contribuições são bem-vindas!