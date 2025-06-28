from fastapi import FastAPI
from app.routers import recomendacoes

app = FastAPI(title="Classificador de Notícias Falsas")

app.include_router(recomendacoes.router, prefix="/api")
