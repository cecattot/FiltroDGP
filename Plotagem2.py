from igraph import *
import pandas as pd
from itertools import combinations
import roman

df = pd.read_csv('pesquisadores.csv')
dfGrupos = pd.read_csv('dados_grupos.csv')
# Mapeamento de cores para cada tipo de pesquisador
cores = {
    "Pesquisador": "blue",
    "TAE": "pink",
    "Estudante": "purple",
    "Colaborador Estrangeiro": "khaki"
}

# Criar o grafo
grafo = Graph()

# Agrupar pesquisadores por grupo
pesquisadores_por_grupo = df.groupby('ID do Grupo').size().to_dict()
grupos_por_pesquisadores = df.groupby('Nome')[['ID do Grupo', 'Tipo']].apply(
    lambda x: list(map(tuple, x.values))).to_dict()

# Mapear IDs de grupos para vértices
grupo_para_vertice = {grupo_id: i for i, grupo_id in enumerate(pesquisadores_por_grupo.keys())}

# Mapear algarismos romanos para os vértices
algarismos_romanos = [roman.toRoman(i+1) for i in range(len(grupo_para_vertice))]

# Adicionar vértices ao grafo para cada grupo, associando algarismos romanos
for grupo_id, vertice_id in grupo_para_vertice.items():
    tamanho_grupo = pesquisadores_por_grupo[grupo_id]
    grafo.add_vertex(name=str(grupo_id), label=algarismos_romanos[vertice_id], size=tamanho_grupo)

# Criar um conjunto de pares de grupos que compartilham pesquisadores
pares_de_grupos_compartilhados = set()
for pesquisador in grupos_por_pesquisadores.values():
    if len(pesquisador) > 1:
        for par in combinations(pesquisador, 2):
            pares_de_grupos_compartilhados.add(par)

# Adicionar arestas entre os grupos que compartilham pesquisadores com cores correspondentes
for grupo1, grupo2 in pares_de_grupos_compartilhados:
    grafo.add_edge(str(grupo1[0]), str(grupo2[0]), color=cores[grupo1[1]])

# Definir visualização do grafo
visual_style = {
    "vertex_size": grafo.vs["size"],  # Define o tamanho dos vértices baseado no tamanho do grupo
    "layout": "kk",  # Usar layout circular para distribuição uniforme dos vértices
    "bbox": (1600, 1600),
    "margin": 20,
    "edge_colors": grafo.es['color'],
    "vertex_label": grafo.vs["label"]  # Adiciona algarismos romanos como rótulos aos vértices
}

plot(grafo, "rede2.pdf", **visual_style)
