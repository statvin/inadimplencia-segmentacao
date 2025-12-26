from pydantic import BaseModel

class ClienteInput(BaseModel):
    score_gravidade: float
    freq_atrasos: float
    razao_pagamento_6m: float
    taxa_uso_limite: float
    limite_credito: float
    canal_preferido: str | None = "WhatsApp"
    cluster: int

class MensagemOutput(BaseModel):
    cluster: int
    perfil_risco: str
    canal: str
    mensagem: str
