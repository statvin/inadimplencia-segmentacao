from fastapi import FastAPI
from src.api.schemas import ClienteInput, MensagemOutput
from src.api.strategy import CLUSTER_LABELS, PROMPTS_POR_CLUSTER
from src.api.llm import gerar_mensagem_llm

app = FastAPI(title="API de Cobrança Inteligente")

@app.post("/gerar-mensagem", response_model=MensagemOutput)
def gerar_mensagem(cliente: ClienteInput):

    perfil = CLUSTER_LABELS[cliente.cluster]
    instrucao = PROMPTS_POR_CLUSTER[cliente.cluster]

    prompt = f"""
Perfil do cliente: {perfil}
Canal: {cliente.canal_preferido}

Dados financeiros:
- Gravidade: {cliente.score_gravidade}
- Frequência: {cliente.freq_atrasos}
- Percentual pago: {cliente.razao_pagamento_6m:.0%}
- Uso do limite: {cliente.taxa_uso_limite:.0%}

TAREFA:
{instrucao}

Gere apenas a mensagem final para o cliente.
"""

    mensagem = gerar_mensagem_llm(prompt)

    return MensagemOutput(
        cluster=cliente.cluster,
        perfil_risco=perfil,
        canal=cliente.canal_preferido,
        mensagem=mensagem
    )
