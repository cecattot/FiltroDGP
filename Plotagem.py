from itertools import combinations
from igraph import *
import pandas as pd

df = pd.read_csv('pesquisadores.csv')
# Criar o grafo
grafo = Graph()

# Adicionar vértices ao grafo e atribuir propriedades
pesquisadores_por_grupo = df.groupby('ID do Grupo')['Nome'].apply(list).to_dict()
for grupo, pesquisadores in pesquisadores_por_grupo.items():
    grafo.add_vertices(pesquisadores)

# Adicionar arestas ao grafo entre pesquisadores do mesmo grupo
for pesquisadores in pesquisadores_por_grupo.values():
    if len(pesquisadores) > 1:
        for par in combinations(pesquisadores, 2):
            grafo.add_edge(par[0], par[1])

# Definir visualização do grafo
visual_style = {
    "vertex_size": 20,
    "layout": "kk",
    "bbox": (1600, 1600),
    "margin": 20
}

# Plotar o grafo
plot(grafo, "rede1.pdf", **visual_style)


#
# Agrupando os pesquisadores por grupo:
# Primeiro, usamos o método groupby do pandas para agrupar os pesquisadores pelo ID do Grupo. Isso cria um dicionário onde as chaves são os IDs do Grupo e os valores são listas dos nomes dos pesquisadores nesse grupo.
# python
# Copy code
# pesquisadores_por_grupo = df.groupby('ID do Grupo')['Nome'].apply(list).to_dict()
# Adicionando vértices ao grafo:
# Para cada grupo, adicionamos todos os pesquisadores desse grupo como vértices no grafo.
# python
# Copy code
# for grupo, pesquisadores in pesquisadores_por_grupo.items():
#     grafo.add_vertices(pesquisadores)
# Adicionando arestas entre pesquisadores do mesmo grupo:
# Para cada grupo, verificamos se há mais de um pesquisador no grupo. Se houver, usamos a função combinations do módulo itertools para gerar todas as combinações possíveis de pares de pesquisadores dentro do grupo. Em seguida, adicionamos uma aresta entre cada par de pesquisadores.
# python
# Copy code
# for pesquisadores in pesquisadores_por_grupo.values():
#     if len(pesquisadores) > 1:
#         for par in combinations(pesquisadores, 2):
#             grafo.add_edge(par[0], par[1])
# Definindo visualização do grafo:
# Definimos algumas opções de visualização para o grafo, como o tamanho do vértice, o layout e a margem.
# python
# Copy code
# visual_style = {
#     "vertex_size": 20,
#     "layout": "kk",
#     "bbox": (1600, 1600),
#     "margin": 20
# }
# Plotando o grafo:
# Finalmente, usamos a função plot do igraph para visualizar o grafo com as opções de estilo que definimos anteriormente.
# python
# Copy code
# plot(grafo, **visual_style)
# Espero que isso ajude a entender como o algoritmo funciona!
#