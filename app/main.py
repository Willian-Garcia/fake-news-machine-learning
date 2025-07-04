from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import recomendacoes
import nltk
nltk.download('punkt')

app = FastAPI(title="Classificador de Notícias Falsas")

# 🔓 Libera acesso CORS para o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recomendacoes.router, prefix="/api")
