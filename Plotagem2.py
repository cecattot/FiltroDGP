from igraph import *
import pandas as pd
from itertools import combinations

df = pd.read_csv('pesquisadores.csv')

# Criar o grafo
grafo = Graph()

# Agrupar pesquisadores por grupo
pesquisadores_por_grupo = df.groupby('ID do Grupo')['Nome'].apply(list).to_dict()

# Mapear IDs de grupos para vértices
grupo_para_vertice = {grupo_id: i for i, grupo_id in enumerate(pesquisadores_por_grupo.keys())}

# Adicionar vértices ao grafo para cada grupo
for grupo_id, vertice_id in grupo_para_vertice.items():
    grafo.add_vertex(name=str(grupo_id))

# Criar um dicionário de pesquisadores para acessar o grupo de um pesquisador
pesquisador_para_grupo = {pesquisador: grupo for grupo, pesquisadores in pesquisadores_por_grupo.items() for pesquisador in pesquisadores}

# Criar um conjunto de pares de grupos que compartilham pesquisadores
pares_de_grupos_compartilhados = set()
for pesquisadores in pesquisadores_por_grupo.values():
    for par in combinations(pesquisadores, 2):
        grupo1 = pesquisador_para_grupo[par[0]]
        grupo2 = pesquisador_para_grupo[par[1]]
        if grupo1 != grupo2:
            pares_de_grupos_compartilhados.add((min(grupo1, grupo2), max(grupo1, grupo2)))

# Adicionar arestas entre os grupos que compartilham pesquisadores
for grupo1, grupo2 in pares_de_grupos_compartilhados:
    grafo.add_edge(str(grupo1), str(grupo2))

# Definir visualização do grafo
visual_style = {
    "vertex_size": 20,
    "layout": "kk",
    "bbox": (1600, 1600),
    "margin": 20
}

plot(grafo, "rede2.pdf", **visual_style)
