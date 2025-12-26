import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib


# -----------------------------
# CONFIGURAÇÕES PADRÃO
# -----------------------------
RANDOM_STATE = 42
DEFAULT_N_CLUSTERS = 4


# -----------------------------
# FEATURE SELECTION
# -----------------------------
def select_features_for_clustering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Seleciona e valida as features finais utilizadas no clustering.

    As features escolhidas representam:
    - Gravidade do atraso (score_gravidade)
    - Capacidade de pagamento (razao_pagamento_6m)
    - Pressão financeira (taxa_uso_limite)
    - Tamanho / relevância do cliente (limite_credito)
    """

    features = [
        "score_gravidade",
        "razao_pagamento_6m",
        "taxa_uso_limite",
        "limite_credito"
    ]

    missing = [f for f in features if f not in df.columns]
    if missing:
        raise ValueError(
            f"Colunas ausentes para clustering: {missing}. "
            f"Verifique se o pipeline de features foi executado corretamente."
        )

    return df[features].copy()


# -----------------------------
# PREPROCESSAMENTO
# -----------------------------
def scale_features(X: pd.DataFrame) -> tuple:
    """
    Padroniza as features para clustering.

    K-Means é sensível à escala. Sem isso, limite_credito dominaria o modelo.
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler


# -----------------------------
# TREINAMENTO DO MODELO
# -----------------------------
def train_kmeans(
    X_scaled: np.ndarray,
    n_clusters: int = DEFAULT_N_CLUSTERS
) -> KMeans:
    """
    Treina o modelo K-Means.
    """
    print(f"⚙️ Treinando KMeans com n_clusters={n_clusters}...")
    model = KMeans(
        n_clusters=n_clusters,
        random_state=RANDOM_STATE,
        n_init=10
    )
    model.fit(X_scaled)
    return model


# -----------------------------
# AVALIAÇÃO DO CLUSTERING
# -----------------------------
def evaluate_clustering(
    X_scaled: np.ndarray,
    labels: np.ndarray
) -> float:
    """
    Avalia a qualidade do clustering usando Silhouette Score.

    Retorna:
        float: silhouette_score
    """
    score = silhouette_score(X_scaled, labels)
    print(f"📊 Silhouette Score: {score:.4f}")
    return score


# -----------------------------
# PÓS-PROCESSAMENTO SEMÂNTICO
# -----------------------------
def reorder_clusters_by_risk(
    df: pd.DataFrame,
    raw_labels: np.ndarray
) -> pd.Series:
    """
    Reordena os clusters de forma semântica, garantindo consistência:

    Cluster 0 -> menor risco
    Cluster N -> maior risco

    Critério:
        média do score_gravidade por cluster
    """
    temp = df.copy()
    temp["cluster_raw"] = raw_labels

    risk_order = (
        temp.groupby("cluster_raw")["score_gravidade"]
        .mean()
        .sort_values()
        .index
    )

    mapping = {old: new for new, old in enumerate(risk_order)}
    return pd.Series(raw_labels).map(mapping)


# -----------------------------
# PIPELINE COMPLETO
# -----------------------------
def run_clustering_pipeline(
    df: pd.DataFrame,
    n_clusters: int = DEFAULT_N_CLUSTERS,
    return_models: bool = False
):
    """
    Executa o pipeline completo de clustering comportamental.

    Etapas:
    1. Seleção de features
    2. Padronização
    3. Treinamento K-Means
    4. Avaliação
    5. Reordenação semântica dos clusters

    Retorna:
        df_clustered (pd.DataFrame)
        [opcional] model, scaler
    """

    # 1. Feature Selection
    X = select_features_for_clustering(df)

    # 2. Scaling
    X_scaled, scaler = scale_features(X)

    # 3. Treinamento
    model = train_kmeans(X_scaled, n_clusters=n_clusters)

    # 4. Avaliação
    evaluate_clustering(X_scaled, model.labels_)

    # 5. Rotulagem semântica
    df_out = df.copy()
    df_out["cluster"] = reorder_clusters_by_risk(df, model.labels_)

    if return_models:
        return df_out, model, scaler

    return df_out


# -----------------------------
# EXECUÇÃO LOCAL (DEBUG)
# -----------------------------
if __name__ == "__main__":
    print("📦 Módulo de clustering carregado com sucesso.")
    print("Use run_clustering_pipeline(df) a partir do notebook.")
