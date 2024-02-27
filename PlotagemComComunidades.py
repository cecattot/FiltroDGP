import random
from itertools import combinations

from igraph import *
import pandas as pd
import roman

# Carregar os dados
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

# Adicionar arestas entre os grupos que compartilham pesquisadores com cores correspondentes
for pesquisador in grupos_por_pesquisadores.values():
    if len(pesquisador) > 1:
        for par in combinations(pesquisador, 2):
            grafo.add_edge(str(par[0][0]), str(par[1][0]), color=cores[par[0][1]])

# Adicionar atributo "Campus" aos vértices
for index, row in dfGrupos.iterrows():
    grupo_id = row['id']
    campus = row['Campus']
    vertice = grafo.vs.find(name=str(grupo_id))
    vertice['campus'] = campus

# Detectar comunidades com base na conexão dos vértices
comunidades = grafo.community_multilevel()

# Definir cores aleatórias para os demais campi
cores_comunidades = {
    "Campus Barra do Garças": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Campus Cáceres": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Campus Campo Novo do Parecis": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Campus Cuiabá": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Campus Juína": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Campus Rondonópolis": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Campus São Vicente": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "IFMT Campus Alta Floresta": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "IFMT Campus Várzea Grande": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "INSTITUTO FEDERAL DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DE MATO GROSSO": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Instituto Federal de Mato Grosso - Campus Bela Vista": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Instituto Federal de Mato Grosso - Campus Confresa": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Instituto Federal de Mato Grosso - Campus Pontes e Lacerda": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Instituto Federal de Mato Grosso - Campus Primavera do Leste": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Instituto Federal de Mato Grosso - Campus Sorriso": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
    "Reitoria": "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
}


# Definir cor dos vértices de acordo com a comunidade
for vertice in grafo.vs:
    campus = vertice['campus']
    cor = cores_comunidades.get(campus, "gray")
    vertice["color"] = cor

# Definir visualização do grafo
visual_style = {
    "vertex_size": grafo.vs["size"],
    "layout": "kk",
    "bbox": (1600, 1600),
    "margin": 20,
    "edge_colors": grafo.es['color'],
    "vertex_label": grafo.vs["label"],
    "vertex_color": grafo.vs["color"]
}

plot(grafo, "rede_com_comunidades.pdf", **visual_style)
