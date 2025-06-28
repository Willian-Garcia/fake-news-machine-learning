from fastapi import APIRouter, HTTPException
from app.schemas.recomendacao import RequisicaoNoticia, RespostaClassificacao
from app.services.recomendacao_service import (
    classificar_texto,
    obter_historico,
    status_modelo,
    pegar_exemplo
)
from typing import List, Dict, Union

router = APIRouter()

@router.post("/classificar-noticia", response_model=RespostaClassificacao)
def classificar(requisicao: RequisicaoNoticia) -> RespostaClassificacao:
    if requisicao.usar_exemplo and requisicao.usar_exemplo.lower() == "true":
        texto, origem, rotulo = pegar_exemplo(retornar_rotulo=True)
        print(f"📌 Exemplo automático carregado de: {origem} | Rótulo esperado: {rotulo}")
    elif requisicao.texto:
        texto = requisicao.texto
    else:
        raise HTTPException(status_code=422, detail="Você deve fornecer um texto.")

    return classificar_texto(texto)

@router.get("/exemplo-noticia", response_model=Dict[str, str])
def exemplo_noticia():
    texto, origem, rotulo = pegar_exemplo(retornar_rotulo=True)
    return {
        "texto": texto,
        "origem": origem,
        "rotulo_esperado": rotulo
    }

@router.get("/historico", response_model=List[RespostaClassificacao])
def historico():
    return obter_historico()

@router.get("/status", response_model=Dict[str, bool])
def status():
    return status_modelo()
