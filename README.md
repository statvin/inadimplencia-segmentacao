# 🏦 Inadimplência • Segmentação Inteligente com ML + LLM

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![LLM](https://img.shields.io/badge/LLM-Groq%20%7C%20LLaMA%203.3-purple)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

---

## 📌 Overview

Este repositório implementa um **sistema de segmentação comportamental de clientes inadimplentes**, projetado para **uso prático em processos de cobrança e gestão de risco**.

A solução combina **Machine Learning não supervisionado**, **regras explícitas de negócio**, **Modelos de Linguagem (LLMs)** e uma **API REST** para transformar dados financeiros em **ações operacionais**, mantendo **explicabilidade, controle e governança**.

---

## 🎯 Problema

Processos tradicionais de cobrança tratam clientes inadimplentes de forma homogênea, o que gera atrito, baixa efetividade e alto custo operacional.  
Este sistema resolve o problema ao **segmentar clientes por comportamento financeiro real**, e não apenas por atraso pontual.

---

## 🧩 Arquitetura Geral

```text
Dados Financeiros Históricos
        ↓
Feature Engineering (Sinais de Risco)
        ↓
Clustering Comportamental (ML)
        ↓
Perfis de Risco Interpretáveis
        ↓
Estratégia de Cobrança (Regras de Negócio)
        ↓
Geração de Mensagens (LLM)
        ↓
API REST
```

---

## 📊 Feature Engineering

Os principais sinais de risco construídos incluem:

- **score_gravidade** — gravidade não linear dos atrasos  
- **freq_atrasos** — recorrência de inadimplência  
- **razao_pagamento_6m** — capacidade efetiva de pagamento  
- **taxa_uso_limite** — proxy de pressão financeira  

Essas variáveis permitem diferenciar atraso ocasional de **inadimplência estrutural**.

---

## 🧠 Clustering Comportamental

- Algoritmo: **KMeans**
- Biblioteca: **scikit-learn**
- Normalização: **StandardScaler**
- Número de clusters: **4**
- Avaliação (a posteriori): **Silhouette Score ≈ 0.39**

### 🔍 Justificativa para `k = 4`

O número de clusters foi definido **a priori**, como uma **hipótese informada pelo domínio do problema**, e não por otimização exaustiva de métricas.

Em contextos operacionais de cobrança, o risco tende a ser tratado em **poucos níveis claramente distinguíveis**, tais como:
- clientes resilientes ou de baixo risco  
- risco leve / comportamento irregular  
- inadimplência recorrente  
- casos críticos de alto risco  

O valor `k = 4` representa o **menor número de grupos capaz de gerar perfis interpretáveis e acionáveis**, mantendo simplicidade operacional.

Após o treinamento, a segmentação apresentou:
- separação estatisticamente aceitável (silhouette ≈ 0.39)  
- coerência semântica entre clusters  
- crescimento monotônico do risco entre grupos  
- estabilidade dos perfis extremos  

Essa abordagem prioriza **interpretação, governança e uso prático**, em vez de maximização puramente métrica.

---

### Perfis Identificados

| Cluster | Perfil de Risco |
|-------|----------------|
| 0 | Baixo risco / Adimplente resiliente |
| 1 | Risco leve / Pagador irregular |
| 2 | Risco recorrente / Pressão financeira |
| 3 | Alto risco / Crítico extremo |

---

## 🎯 Estratégia de Cobrança

A política de cobrança é definida por **regras explícitas**, fora do LLM:

| Perfil | Objetivo | Canal | Tom |
|------|---------|-------|-----|
| Baixo risco | Prevenção | Email | Preventivo |
| Risco leve | Regularização | WhatsApp | Objetivo |
| Risco recorrente | Negociação | WhatsApp | Empático |
| Crítico | Mitigação de perda | Telefone | Firme |

O LLM **executa a comunicação**, mas **não toma decisões de negócio**.

---

## 🤖 LLM

- Provedor: **Groq**
- Modelo: **LLaMA 3.3 70B**
- Uso: geração de mensagens alinhadas ao perfil de risco e à estratégia definida

---

## 🚀 API REST

A solução é exposta via **FastAPI**.

### Endpoint principal

```http
POST /gerar-mensagem
```

---

## 🔐 Segurança

Variáveis sensíveis (ex.: chaves de API) **não são armazenadas no código ou no repositório**.

Elas são carregadas exclusivamente via **variáveis de ambiente**:

```bash
export GROQ_API_KEY=your_api_key_here
```

Arquivos `.env` estão incluídos no `.gitignore` e **não são versionados**.

---

## 🛠️ Stack

- Python 3.10+
- Pandas / NumPy
- scikit-learn
- FastAPI
- Groq API
- LLaMA 3.3

---

## 📁 Estrutura do Projeto

```text
├── src/
│   ├── api/
│   ├── clustering.py
│   ├── features.py
│   └── data_loader.py
├── notebooks/
├── data/
└── README.md
```

---

## 📌 Observação Final

Este projeto demonstra uma aplicação prática de **ML explicável e LLMs** em um cenário realista de **gestão de inadimplência**, priorizando **clareza, controle e acionabilidade**, em vez de otimização puramente acadêmica.
