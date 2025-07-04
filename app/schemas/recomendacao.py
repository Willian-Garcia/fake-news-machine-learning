from pydantic import BaseModel
from typing import List, Optional

class RequisicaoNoticia(BaseModel):
    texto: str  # obrigatório
    usar_exemplo: bool  # string fixa como "false"

    class Config:
        schema_extra = {
            "example": {
                "texto": "NASA confirms the discovery of a new planet.",
                "usar_exemplo": "false"
            }
        }

class RespostaClassificacao(BaseModel):
    classe: str
    probabilidade: float
    palavras_influentes: List[str]
