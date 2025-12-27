import pandas as pd

# Estratégia fixa por cluster
# Fonte única de verdade para API, Streamlit e notebooks

estrategia_cluster = pd.DataFrame({
    "perfil_risco": [
        "Baixo risco / Adimplente resiliente",
        "Risco leve / Pagador irregular",
        "Risco recorrente / Pressão financeira",
        "Alto risco / Crítico extremo"
    ],
    "objetivo_cobranca": [
        "Prevenção e educação financeira",
        "Regularização pontual",
        "Negociação ativa",
        "Mitigação de perda"
    ],
    "canal_prioritario": [
        "Email",
        "WhatsApp",
        "WhatsApp",
        "Telefone"
    ],
    "tom_comunicacao": [
        "Preventivo e cordial",
        "Objetivo e respeitoso",
        "Empático e negociador",
        "Firme e direto"
    ],
    "acao_recomendada": [
        "Lembrete + orientação",
        "Aviso de vencimento + CTA simples",
        "Proposta de parcelamento / acordo",
        "Escalonar para atendimento humano"
    ]
}, index=[0, 1, 2, 3])
