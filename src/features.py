import pandas as pd
import numpy as np

def calculate_risk_features(df):
    """
    Feature Engineering com Ponderação de Risco (Approach Sênior).
    Evita tratar variáveis ordinais como intervalares lineares.
    """
    df_feat = df.copy()
    
    # Colunas de status de pagamento (Setembro a Abril)
    pay_cols = [c for c in df_feat.columns if 'status_pag_' in c]
    
    # --- 1. Score de Gravidade (Weighted Delay) ---
    # Lógica: Atrasos longos (3, 4) são exponencialmente piores que curtos (1).
    # Transformação: x^2 para valores > 0.
    # Exemplo: 
    #   Cliente A (3 meses atraso): 3^2 = 9 pontos
    #   Cliente B (3x 1 mês atraso): 1^2 + 1^2 + 1^2 = 3 pontos
    
    def weighted_risk(row):
        # Pega apenas os valores que indicam atraso real (>0)
        delays = [x for x in row if x > 0]
        if not delays:
            return 0
        # Soma dos quadrados dos atrasos
        return sum([d**2 for d in delays])

    df_feat['score_gravidade'] = df_feat[pay_cols].apply(weighted_risk, axis=1)

    # --- 2. Recorrência (Frequência) ---
    # Quantas vezes ele atrasou, independente da gravidade?
    # Isso separa o "deslize pontual" do "hábito".
    df_feat['freq_atrasos'] = df_feat[pay_cols].apply(lambda row: sum([1 for x in row if x > 0]), axis=1)

    # --- 3. Uso do Limite (Pressão Financeira) ---
    # bill_amt1 pode ser negativo (crédito), então tratamos
    df_feat['taxa_uso_limite'] = (
    df_feat['bill_amt1'] / df_feat['limite_credito'].replace(0, 1)).clip(lower=0, upper=1.5)

    
    # 4. Proto-Feature: Razão Pagamento (Capacidade de Honrar)
    # Quanto pagou / Quanto devia (Soma 6 meses para suavizar volatilidade)
    bill_cols = [c for c in df_feat.columns if 'bill_amt' in c]
    pay_amt_cols = [c for c in df_feat.columns if 'pay_amt' in c]
    
    total_bill = df_feat[bill_cols].sum(axis=1)
    total_pay = df_feat[pay_amt_cols].sum(axis=1)
    
    # Evita divisão por zero e clipa em 1 (se pagou a mais, é 100%)
    df_feat['razao_pagamento_6m'] = np.where(total_bill > 0, total_pay / total_bill, 1)
    df_feat['razao_pagamento_6m'] = df_feat['razao_pagamento_6m'].clip(0, 1)

    return df_feat

def simulate_collection_data(df):
    """
    Gera dados sintéticos de CRM para a estratégia de cobrança (LLM).
    Mantém a lógica anterior de canais.
    """
    np.random.seed(42)
    n = len(df)
    
    # 1. Canal Preferido (Proxy de Idade)
    canais = ['WhatsApp', 'SMS', 'Email', 'Telefone']
    if 'idade' in df.columns:
        df['canal_preferido'] = df['idade'].apply(
            lambda x: np.random.choice(canais, p=[0.5, 0.3, 0.15, 0.05]) if x < 30 
            else np.random.choice(canais, p=[0.1, 0.2, 0.3, 0.4])
        )
    else:
        df['canal_preferido'] = np.random.choice(canais, size=n)

    # 2. Perfil de Atendimento (Engajamento)
    # Probabilidade baseada no risco real (target)
    prob_atender = np.where(df['is_inadimplente'] == 1, 0.15, 0.65)
    df['atende_cobranca'] = np.random.rand(n) < prob_atender
    df['perfil_atendimento'] = df['atende_cobranca'].map({True: 'Engajado', False: 'Evasivo'})
    
    return df

def process_pipeline(df):
    # Limpeza de colunas técnicas
    if 'id' in df.columns: df = df.drop(columns=['id'])
    for col in df.columns:
        if 'unnamed' in col.lower():
            df = df.drop(columns=[col])

    # Feature Engineering
    df = calculate_risk_features(df)
    df = simulate_collection_data(df)
    
    return df