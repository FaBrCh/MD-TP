# Fase 1: Proposta

## Trabalho de Mineração de Dados: Agrupamento (Clusterização)

Alunos: Dara Oliveira e Fabrício Costa

## Objetivo do Trabalho

O objetivo deste trabalho é aplicar técnicas de agrupamento (clusterização) para explorar padrões ocultos nos dados. Serão utilizados algoritmos de machine learning não supervisionados. Através da análise dos agrupamentos, busca-se obter insights relevantes que ajudem a compreender perfis, padrões de comportamento ou características específicas presentes nos dados.

## Contexto do Problema

Escolheu-se trabalhar com um conjunto de dados de clientes de uma instituição bancária. O *dataset* contém informações demográficas e financeiras dos clientes, além de indicar se aceitaram ou não uma proposta de produto financeiro (um depósito a prazo).

O problema de negócio consiste em entender os diferentes perfis de clientes, agrupando-os por características similares. Isso pode auxiliar o banco a criar estratégias mais personalizadas para marketing, retenção e desenvolvimento de produtos.

## Por que a Tarefa é Relevante e Significativa?

A tarefa é relevante porque permite às empresas, neste caso, uma instituição financeira, entender melhor seus clientes, segmentando-os com base em características semelhantes. Isso possibilita:

*   Estratégias de marketing mais eficientes;
*   Ofertas de produtos e serviços personalizadas;
*   Otimização de recursos e aumento da satisfação do cliente;
*   Maior taxa de conversão em campanhas.

Além disso, o uso de agrupamento é extremamente valioso em cenários onde não existe uma variável resposta clara, mas onde é necessário identificar padrões e segmentos de forma exploratória.

## Descrição dos Dados

### Origem do Dataset

O *dataset* foi disponibilizado publicamente no repositório da UCI Machine Learning Repository, conhecido como "Bank Marketing".

Link: [https://archive.ics.uci.edu/ml/datasets/bank+marketing](https://archive.ics.uci.edu/ml/datasets/bank+marketing)

Ele foi coletado a partir de campanhas de marketing telefônico realizadas por um banco português, com o objetivo de oferecer depósitos a prazo aos seus clientes.

### Características do Dataset

*Descritiva* (Esta é uma menção genérica sobre o tipo de dados, indicando que são descritivos dos clientes e campanhas).

## Relação com o Problema de Negócio

Este *dataset* permite agrupar os clientes de acordo com características socioeconômicas, comportamento bancário e histórico de campanhas de marketing. A análise por agrupamento pode revelar, por exemplo:

*   Perfis de clientes mais propensos a aderirem a produtos financeiros;
*   Grupos que apresentam maior resistência a campanhas;
*   Segmentos com características de risco financeiro.

Estes *insights* podem ser aplicados diretamente na tomada de decisão para estratégias de marketing, gestão de risco e desenvolvimento de produtos no setor bancário.

## Como a Tarefa Será Executada

1.  **Entendimento dos Dados:**
    *   Análise exploratória das variáveis.
    *   Avaliação da necessidade de transformação (ex.: variáveis categóricas em numéricas).

2.  **Preparação dos Dados:**
    *   Tratamento de valores nulos (se houver).
    *   Normalização de variáveis numéricas.
    *   Codificação de variáveis categóricas (One-Hot Encoding ou Label Encoding).
    *   Seleção das *features* mais relevantes para o agrupamento.

3.  **Modelagem (Agrupamento):**
    Serão aplicados os seguintes algoritmos de clusterização:
    *   K-Means (análise de grupos bem definidos e centrados)
    *   DBSCAN (descoberta de grupos com formas arbitrárias e tratamento de ruído)
    *   Hierárquico (para construção de dendrogramas e análise hierárquica dos *clusters*)

4.  **Avaliação dos Resultados:**
    *   Análise dos *clusters* formados.
    *   Interpretação dos perfis de clientes presentes em cada *cluster*.
    *   Discussão sobre como esses agrupamentos podem ser utilizados na prática pelo negócio.

## Conclusão da Fase 1

O trabalho utilizará técnicas de agrupamento aplicadas a dados bancários reais, com o objetivo de identificar perfis de clientes e gerar *insights* que contribuam para a tomada de decisões no setor financeiro. Esta fase inicial permite estabelecer o contexto, definir os objetivos e compreender as características dos dados, servindo como base para as próximas etapas do projeto.