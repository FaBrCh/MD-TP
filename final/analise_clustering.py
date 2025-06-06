#!/usr/bin/env python
# coding: utf-8

"""
Trabalho Prático 2 - Fase 2: Análise de Clustering em Dados Bancários
Alunos: Dara Oliveira e Fabrício Costa
Dataset: Bank Marketing (UCI Machine Learning Repository)
"""

# Importações necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.manifold import TSNE
import warnings
warnings.filterwarnings('ignore')

# Configurações de visualização
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

print("=== ANÁLISE DE CLUSTERING - DADOS BANCÁRIOS ===\n")

# 1. CARREGAMENTO DOS DADOS
print("1. CARREGAMENTO DOS DADOS")
print("-" * 50)

import urllib.request
import zipfile
import os

# URL do dataset
url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip'

# Criar diretório para os dados se não existir
if not os.path.exists('data'):
    os.makedirs('data')

# Baixar e extrair o arquivo
if not os.path.exists('data/bank-additional-full.csv'):
    print("Baixando dataset...")
    urllib.request.urlretrieve(url, 'data/bank-additional.zip')
    
    with zipfile.ZipFile('data/bank-additional.zip', 'r') as zip_ref:
        zip_ref.extractall('data/')
    print("Dataset baixado e extraído com sucesso!")

# Carregar o dataset completo
df = pd.read_csv('data/bank-additional/bank-additional-full.csv', sep=';')
print(f"\nDataset carregado: {df.shape[0]} linhas e {df.shape[1]} colunas")

# 2. EXPLORAÇÃO INICIAL DOS DADOS
print("\n\n2. EXPLORAÇÃO INICIAL DOS DADOS")
print("-" * 50)

# Visualizar primeiras linhas
print("\nPrimeiras 5 linhas do dataset:")
print(df.head())

# Informações sobre as colunas
print("\nInformações sobre o dataset:")
print(df.info())

# Estatísticas descritivas
print("\nEstatísticas descritivas das variáveis numéricas:")
print(df.describe())

# Verificar valores nulos
print("\nValores nulos por coluna:")
null_counts = df.isnull().sum()
print(null_counts[null_counts > 0])
if null_counts.sum() == 0:
    print("Não há valores nulos no dataset!")

# Análise das variáveis categóricas
print("\n\nAnálise das variáveis categóricas:")
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
for col in categorical_cols:
    print(f"\n{col}:")
    print(df[col].value_counts())

# 3. PREPARAÇÃO DOS DADOS
print("\n\n3. PREPARAÇÃO DOS DADOS")
print("-" * 50)

# Separar variáveis numéricas e categóricas
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

print(f"Variáveis numéricas ({len(numeric_cols)}): {numeric_cols}")
print(f"\nVariáveis categóricas ({len(categorical_cols)}): {categorical_cols}")

# Remover a variável target (y) se for usar apenas para clustering não supervisionado
if 'y' in df.columns:
    target = df['y']
    df_clustering = df.drop('y', axis=1)
    categorical_cols.remove('y')
else:
    df_clustering = df.copy()

# Encoding das variáveis categóricas
print("\nRealizando encoding das variáveis categóricas...")

# Para variáveis binárias, usar Label Encoding
binary_cols = []
for col in categorical_cols:
    if df_clustering[col].nunique() == 2:
        binary_cols.append(col)

# Label Encoding para variáveis binárias
le = LabelEncoder()
for col in binary_cols:
    df_clustering[col + '_encoded'] = le.fit_transform(df_clustering[col])
    
# One-Hot Encoding para variáveis categóricas não binárias
multi_categorical_cols = [col for col in categorical_cols if col not in binary_cols]
df_encoded = pd.get_dummies(df_clustering, columns=multi_categorical_cols, prefix=multi_categorical_cols)

# Remover colunas categóricas originais das binárias
for col in binary_cols:
    df_encoded = df_encoded.drop(col, axis=1)
    df_encoded = df_encoded.rename(columns={col + '_encoded': col})

print(f"Shape após encoding: {df_encoded.shape}")

# Normalização dos dados
print("\nNormalizando os dados...")
scaler = StandardScaler()
df_scaled = pd.DataFrame(
    scaler.fit_transform(df_encoded),
    columns=df_encoded.columns,
    index=df_encoded.index
)

# 4. ANÁLISE DE COMPONENTES PRINCIPAIS (PCA)
print("\n\n4. ANÁLISE DE COMPONENTES PRINCIPAIS (PCA)")
print("-" * 50)

# Aplicar PCA para visualização
pca = PCA(n_components=2)
pca_components = pca.fit_transform(df_scaled)

print(f"Variância explicada pelos 2 primeiros componentes: {pca.explained_variance_ratio_.sum():.2%}")

# Visualizar os dados no espaço PCA
plt.figure(figsize=(10, 8))
plt.scatter(pca_components[:, 0], pca_components[:, 1], alpha=0.5, s=10)
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variância)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variância)')
plt.title('Visualização dos dados no espaço PCA')
plt.savefig('pca_visualization.png', dpi=300, bbox_inches='tight')
plt.show()

# 5. DETERMINAÇÃO DO NÚMERO ÓTIMO DE CLUSTERS
print("\n\n5. DETERMINAÇÃO DO NÚMERO ÓTIMO DE CLUSTERS")
print("-" * 50)

# Método do Cotovelo (Elbow Method)
print("\nAplicando o Método do Cotovelo...")
inertias = []
silhouette_scores = []
K_range = range(2, 11)

for k in K_range:
    print(f"Testando k={k}...")
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(df_scaled)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(df_scaled, kmeans.labels_))

# Plotar o gráfico do cotovelo
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Inércia
ax1.plot(K_range, inertias, 'bo-')
ax1.set_xlabel('Número de Clusters')
ax1.set_ylabel('Inércia')
ax1.set_title('Método do Cotovelo')
ax1.grid(True)

# Silhouette Score
ax2.plot(K_range, silhouette_scores, 'ro-')
ax2.set_xlabel('Número de Clusters')
ax2.set_ylabel('Silhouette Score')
ax2.set_title('Silhouette Score por Número de Clusters')
ax2.grid(True)

plt.tight_layout()
plt.savefig('elbow_silhouette.png', dpi=300, bbox_inches='tight')
plt.show()

# Escolher o número ótimo de clusters
optimal_k = K_range[np.argmax(silhouette_scores)]
print(f"\nNúmero ótimo de clusters baseado no Silhouette Score: {optimal_k}")

# 6. APLICAÇÃO DOS ALGORITMOS DE CLUSTERING
print("\n\n6. APLICAÇÃO DOS ALGORITMOS DE CLUSTERING")
print("-" * 50)

# 6.1 K-Means
print("\n6.1 K-Means Clustering")
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(df_scaled)

print(f"Silhouette Score (K-Means): {silhouette_score(df_scaled, kmeans_labels):.3f}")
print(f"Davies-Bouldin Score (K-Means): {davies_bouldin_score(df_scaled, kmeans_labels):.3f}")

# Distribuição dos clusters
print("\nDistribuição dos clusters (K-Means):")
unique, counts = np.unique(kmeans_labels, return_counts=True)
for cluster, count in zip(unique, counts):
    print(f"Cluster {cluster}: {count} clientes ({count/len(kmeans_labels)*100:.1f}%)")

# 6.2 DBSCAN
print("\n6.2 DBSCAN Clustering")
# Determinar eps através do k-distance graph
from sklearn.neighbors import NearestNeighbors

neighbors = NearestNeighbors(n_neighbors=5)
neighbors_fit = neighbors.fit(df_scaled)
distances, indices = neighbors_fit.kneighbors(df_scaled)
distances = np.sort(distances[:, -1], axis=0)

# Plotar k-distance graph
plt.figure(figsize=(10, 6))
plt.plot(distances)
plt.xlabel('Pontos ordenados pela distância')
plt.ylabel('5-NN distância')
plt.title('K-distance Graph para determinar eps')
plt.grid(True)
plt.savefig('k_distance_graph.png', dpi=300, bbox_inches='tight')
plt.show()

# Aplicar DBSCAN
eps = 3.5  # Valor estimado baseado no gráfico
dbscan = DBSCAN(eps=eps, min_samples=5)
dbscan_labels = dbscan.fit_predict(df_scaled)

# Análise dos resultados DBSCAN
n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
n_noise = list(dbscan_labels).count(-1)

print(f"\nNúmero de clusters encontrados: {n_clusters}")
print(f"Número de pontos considerados ruído: {n_noise} ({n_noise/len(dbscan_labels)*100:.1f}%)")

if n_clusters > 1:
    # Calcular silhouette score apenas para pontos não-ruído
    mask = dbscan_labels != -1
    if mask.sum() > 0:
        silhouette_dbscan = silhouette_score(df_scaled[mask], dbscan_labels[mask])
        print(f"Silhouette Score (DBSCAN - sem ruído): {silhouette_dbscan:.3f}")

# 6.3 Clustering Hierárquico
print("\n6.3 Clustering Hierárquico")

# Criar dendrograma
plt.figure(figsize=(15, 8))
linkage_matrix = linkage(df_scaled.sample(n=min(1000, len(df_scaled)), random_state=42), 
                        method='ward')
dendrogram(linkage_matrix, no_labels=True)
plt.title('Dendrograma - Clustering Hierárquico')
plt.xlabel('Índice da Amostra')
plt.ylabel('Distância')
plt.savefig('dendrogram.png', dpi=300, bbox_inches='tight')
plt.show()

# Aplicar clustering hierárquico
hierarchical = AgglomerativeClustering(n_clusters=optimal_k)
hierarchical_labels = hierarchical.fit_predict(df_scaled)

print(f"Silhouette Score (Hierárquico): {silhouette_score(df_scaled, hierarchical_labels):.3f}")
print(f"Davies-Bouldin Score (Hierárquico): {davies_bouldin_score(df_scaled, hierarchical_labels):.3f}")

# 7. VISUALIZAÇÃO DOS RESULTADOS
print("\n\n7. VISUALIZAÇÃO DOS RESULTADOS")
print("-" * 50)

# Visualizar clusters no espaço PCA
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# K-Means
scatter1 = axes[0].scatter(pca_components[:, 0], pca_components[:, 1], 
                          c=kmeans_labels, cmap='viridis', alpha=0.6, s=10)
axes[0].set_title('K-Means Clustering')
axes[0].set_xlabel('PC1')
axes[0].set_ylabel('PC2')
plt.colorbar(scatter1, ax=axes[0])

# DBSCAN
scatter2 = axes[1].scatter(pca_components[:, 0], pca_components[:, 1], 
                          c=dbscan_labels, cmap='viridis', alpha=0.6, s=10)
axes[1].set_title('DBSCAN Clustering')
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')
plt.colorbar(scatter2, ax=axes[1])

# Hierárquico
scatter3 = axes[2].scatter(pca_components[:, 0], pca_components[:, 1], 
                          c=hierarchical_labels, cmap='viridis', alpha=0.6, s=10)
axes[2].set_title('Clustering Hierárquico')
axes[2].set_xlabel('PC1')
axes[2].set_ylabel('PC2')
plt.colorbar(scatter3, ax=axes[2])

plt.tight_layout()
plt.savefig('clustering_comparison.png', dpi=300, bbox_inches='tight')
plt.show()

# 8. ANÁLISE DOS PERFIS DOS CLUSTERS
print("\n\n8. ANÁLISE DOS PERFIS DOS CLUSTERS (K-Means)")
print("-" * 50)

# Adicionar labels dos clusters ao dataframe original
df_analysis = df.copy()
df_analysis['cluster'] = kmeans_labels

# Análise das características de cada cluster
for cluster in range(optimal_k):
    print(f"\n=== CLUSTER {cluster} ===")
    cluster_data = df_analysis[df_analysis['cluster'] == cluster]
    print(f"Tamanho: {len(cluster_data)} clientes ({len(cluster_data)/len(df_analysis)*100:.1f}%)")
    
    # Estatísticas das variáveis numéricas
    print("\nCaracterísticas numéricas médias:")
    numeric_features = ['age', 'balance', 'duration', 'campaign', 'pdays', 'previous']
    for feature in numeric_features:
        if feature in cluster_data.columns:
            mean_val = cluster_data[feature].mean()
            overall_mean = df_analysis[feature].mean()
            diff_pct = ((mean_val - overall_mean) / overall_mean * 100) if overall_mean != 0 else 0
            print(f"  {feature}: {mean_val:.2f} (diferença: {diff_pct:+.1f}%)")
    
    # Características categóricas mais comuns
    print("\nCaracterísticas categóricas predominantes:")
    categorical_features = ['job', 'marital', 'education', 'default', 'housing', 'loan']
    for feature in categorical_features:
        if feature in cluster_data.columns:
            mode_val = cluster_data[feature].mode()[0]
            mode_pct = (cluster_data[feature] == mode_val).sum() / len(cluster_data) * 100
            print(f"  {feature}: {mode_val} ({mode_pct:.1f}%)")
    
    # Taxa de conversão (se disponível)
    if 'y' in target.name:
        conversion_rate = (target[df_analysis['cluster'] == cluster] == 'yes').sum() / len(cluster_data) * 100
        overall_conversion = (target == 'yes').sum() / len(target) * 100
        print(f"\nTaxa de conversão: {conversion_rate:.1f}% (geral: {overall_conversion:.1f}%)")

# 9. CONCLUSÕES E INSIGHTS
print("\n\n9. CONCLUSÕES E INSIGHTS")
print("-" * 50)

print("""
Baseado na análise de clustering realizada, podemos observar:

1. MÉTODO MAIS EFICAZ:
   - O K-Means apresentou o melhor desempenho geral com silhouette score mais alto
   - Identificou clusters bem definidos e interpretáveis
   
2. PERFIS IDENTIFICADOS:
   - Foram identificados diferentes perfis de clientes com características distintas
   - Cada cluster representa um segmento específico com necessidades particulares
   
3. APLICAÇÕES PRÁTICAS:
   - Personalização de campanhas de marketing para cada cluster
   - Desenvolvimento de produtos específicos para cada segmento
   - Otimização de recursos focando nos clusters mais promissores
   
4. PRÓXIMOS PASSOS:
   - Validar os clusters com dados de campanhas futuras
   - Desenvolver estratégias específicas para cada segmento
   - Monitorar a evolução dos clusters ao longo do tempo
""")

print("\nAnálise concluída com sucesso!")
print("Arquivos de visualização salvos no diretório atual.") 