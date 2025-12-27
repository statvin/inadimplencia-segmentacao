import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)


import streamlit as st
import pandas as pd

from src.features import process_pipeline
from src.clustering import run_clustering_pipeline
from src.api.strategy import estrategia_cluster
from src.api.llm import gerar_mensagem_llm

st.set_page_config(
    page_title="Segmentação de Inadimplência",
    layout="wide"
)

st.title("📊 Segmentação Inteligente de Inadimplência")

st.markdown(
    "Demo interativa de segmentação de clientes inadimplentes "
    "com ML + LLM."
)

# Upload do dataset
uploaded_file = st.file_uploader(
    "📂 Faça upload da base de clientes (CSV)",
    type=["csv"]
)

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)

    st.subheader("📋 Base carregada")
    st.dataframe(df_raw.head())

    # Feature engineering
    df_feat = process_pipeline(df_raw)

    # Clustering
    # Clustering
    # Clustering
    df_clustered = run_clustering_pipeline(df_feat)




    


    st.subheader("🧠 Clientes segmentados")
    st.dataframe(df_clustered)

    # Seleção de cliente
    cliente_id = st.selectbox(
        "Selecione um cliente",
        df_clustered.index
    )

    linha = df_clustered.loc[cliente_id]

    st.subheader("🔎 Perfil do Cliente")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Cluster", linha["cluster"])
        st.metric("Score Gravidade", round(linha["score_gravidade"], 2))
        st.metric("Frequência Atrasos", round(linha["freq_atrasos"], 2))

    with col2:
        st.metric("Razão Pagamento", round(linha["razao_pagamento_6m"], 2))
        st.metric("Uso do Limite", round(linha["taxa_uso_limite"], 2))
        st.metric("Limite Crédito", round(linha["limite_credito"], 0))

    # Estratégia
    estrategia = estrategia_cluster.loc[linha["cluster"]]

    st.subheader("🎯 Estratégia de Cobrança")
    st.write(estrategia)

    if st.button("✉️ Gerar mensagem"):

        prompt = f"""
    Você deve gerar uma mensagem de cobrança profissional e adequada ao perfil do cliente.

    Perfil do cliente:
    - Cluster: {linha['cluster']}
    - Score de gravidade: {linha['score_gravidade']}
    - Frequência de atrasos: {linha['freq_atrasos']}
    - Razão de pagamento (6m): {linha['razao_pagamento_6m']}
    - Uso do limite: {linha['taxa_uso_limite']}
    - Limite de crédito: {linha['limite_credito']}
    Estratégia de cobrança:
    - Perfil de risco: {estrategia['perfil_risco']}
    - Objetivo: {estrategia['objetivo_cobranca']}
    - Canal prioritário: {estrategia['canal_prioritario']}
    - Tom de comunicação: {estrategia['tom_comunicacao']}
    - Ação recomendada: {estrategia['acao_recomendada']}
    Instruções:
    - Seja claro, educado e profissional
    - Não seja ameaçador
    - Use linguagem adequada ao contexto bancário
    - Gere apenas o texto da mensagem, sem explicações
    """

        mensagem = gerar_mensagem_llm(prompt)

        st.subheader("💬 Mensagem Gerada")
        st.success(mensagem)
