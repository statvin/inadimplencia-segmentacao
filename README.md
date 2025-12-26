📌 Sistema de Segmentação e Cobrança Inteligente com ML + LLM
🧠 Descrição do Projeto

Este projeto implementa um sistema completo de segmentação comportamental de clientes inadimplentes, com foco em uso operacional em processos de cobrança.

A solução combina:

Machine Learning não supervisionado para segmentação de risco,

regras explícitas de negócio para definição de estratégia,

LLMs para geração de mensagens personalizadas,

e uma API REST pronta para integração com canais como WhatsApp, Email ou CRM.

O objetivo é transformar dados financeiros históricos em ações de cobrança diferenciadas, mantendo explicabilidade, governança e controle do processo.

🎯 Problema Resolvido

Processos tradicionais de cobrança tratam clientes inadimplentes de forma homogênea, o que gera:

atrito desnecessário com bons clientes,

baixa efetividade com clientes recorrentes,

alto custo operacional em casos críticos.

Este sistema resolve isso ao:

segmentar clientes por comportamento real, não apenas por atraso,

definir estratégias específicas por perfil de risco,

automatizar a comunicação, mantendo controle institucional.

🧩 Visão Geral da Arquitetura
Dados Financeiros Históricos
        ↓
Feature Engineering (sinais de risco)
        ↓
Clustering Comportamental (ML)
        ↓
Perfis de Risco Interpretáveis
        ↓
Estratégia de Cobrança por Perfil
        ↓
Geração de Mensagens via LLM
        ↓
API REST para Integração


A arquitetura separa claramente:

modelagem de risco

decisão de negócio

comunicação com o cliente

📊 Modelagem de Risco (Feature Engineering)

O sistema constrói sinais de risco a partir do histórico financeiro do cliente, incluindo:

Gravidade dos atrasos
Penalização não linear para atrasos prolongados.

Frequência de inadimplência
Diferencia atraso pontual de comportamento recorrente.

Capacidade de pagamento
Relação entre valores pagos e devidos.

Pressão financeira
Uso do limite de crédito como proxy de estresse financeiro.

Esses sinais permitem distinguir:

desorganização financeira temporária

incapacidade estrutural de pagamento

🧠 Segmentação Comportamental

Algoritmo: KMeans

Biblioteca: scikit-learn

Padronização: StandardScaler

Número de clusters: 4

Avaliação: Silhouette Score ≈ 0.39

Perfis Gerados
Cluster	Perfil
0	Baixo risco / Adimplente resiliente
1	Risco leve / Pagador irregular
2	Risco recorrente / Pressão financeira
3	Alto risco / Crítico extremo

Os clusters são ordenados semanticamente por risco, garantindo consistência e estabilidade para uso operacional.

✅ Validação

A segmentação foi validada contra a inadimplência real, apresentando:

crescimento monotônico da taxa de default entre clusters,

separação clara entre perfis,

coerência estatística e comportamental.

O clustering captura padrões de comportamento, não apenas o rótulo final.

🎯 Estratégia de Cobrança

A política de cobrança é definida fora do LLM, de forma explícita:

Perfil	Objetivo	Canal	Tom
Baixo risco	Prevenção	Email	Preventivo
Risco leve	Regularização	WhatsApp	Objetivo
Risco recorrente	Negociação	WhatsApp	Empático
Crítico	Mitigação de perda	Telefone	Firme

Essa separação garante:

governança,

auditabilidade,

previsibilidade do sistema.

🤖 Geração de Mensagens (LLM)

Provedor: Groq

Modelo: LLaMA 3.3 70B

Função do LLM:

gerar mensagens alinhadas à estratégia definida,

adaptar tom e linguagem ao perfil de risco,

manter comunicação ética e institucional.

O LLM não toma decisões de negócio.

🚀 API REST

O sistema é exposto via FastAPI, permitindo integração com sistemas externos.

Endpoint principal
POST /gerar-mensagem

Exemplo de Request
{
  "score_gravidade": 5.6,
  "freq_atrasos": 1.2,
  "razao_pagamento_6m": 0.08,
  "taxa_uso_limite": 0.74,
  "limite_credito": 80000,
  "cluster": 2,
  "canal_preferido": "WhatsApp"
}

Exemplo de Response
{
  "cluster": 2,
  "perfil_risco": "Risco recorrente / Pressão financeira",
  "canal": "WhatsApp",
  "mensagem": "Olá, percebemos que..."
}

🛠️ Stack Tecnológica

Python 3

Pandas / NumPy

Scikit-learn

FastAPI

Groq API

LLaMA 3.3

Jupyter Notebook

📁 Estrutura do Projeto
├── src/
│   ├── api/
│   ├── clustering.py
│   ├── features.py
│   └── data_loader.py
├── notebooks/
├── data/
└── README.md

🔮 Possíveis Extensões

Integração com WhatsApp (Typebot / Evolution API)

Deploy em VPS ou Cloud

A/B testing de mensagens

Feedback loop com resposta do cliente

Persistência de decisões em banco de dados

📌 Considerações Finais

Este projeto demonstra a aplicação prática de ML explicável e LLMs em um contexto realista de gestão de inadimplência, com foco em ação, controle e escalabilidade, e não apenas em modelagem.