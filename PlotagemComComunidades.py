import random
from itertools import combinations

from igraph import *
import pandas as pd
import roman
import random
random.seed(42)  # Definindo a semente aleatória

# Carregar os dados
df = pd.read_csv('pesquisadores.csv')
dfGrupos = pd.read_csv('dados_grupos.csv')

# Mapeamento de cores para cada tipo de pesquisador
cores = {
    "Pesquisador": "blue",
    "TAE": "red",
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

# Criar um dicionário para rastrear a contagem de pares de grupos compartilhados
contagem_pares = {}

# Adicionar arestas entre os grupos que compartilham pesquisadores com cores correspondentes
for grupo1, grupo2 in pares_de_grupos_compartilhados:
    par = tuple(sorted([grupo1[0], grupo2[0]]))  # Ordenar o par para garantir consistência
    if par in contagem_pares:
        contagem_pares[par] += 1
    else:
        contagem_pares[par] = 1

    peso = contagem_pares[par]
    grafo.add_edge(str(grupo1[0]), str(grupo2[0]), color=cores[grupo1[1]], weight=peso)

# Adicionar atributo "Campus" aos vértices
for index, row in dfGrupos.iterrows():
    grupo_id = row['id']
    campus = row['Campus']
    vertice = grafo.vs.find(name=str(grupo_id))
    vertice['campus'] = campus

# Definir cores para os campi
# Lista de cores disponíveis em hexadecimal
cores_disponiveis = ["#FF5733", "#FFBD33", "#FF3385", "#33FF57", "#33B0FF",
                     "#B033FF", "#33FFBD", "#FF33E9", "#33FFA8", "#A833FF",
                     "#FF336A", "#33FFC5", "#FFC533", "#3385FF", "#FFE933",
                     "#33FFD8", "#FF33A8", "#33FF71", "#FF33C5"]

# Mapeamento de cores para as chaves
cores_comunidades = {
    "BAG": cores_disponiveis[0],
    "CAS": cores_disponiveis[1],
    "CNP": cores_disponiveis[2],
    "CBA": cores_disponiveis[3],
    "JNA": cores_disponiveis[4],
    "LRV": cores_disponiveis[5],
    "ROO": cores_disponiveis[6],
    "SVC": cores_disponiveis[7],
    "ALF": cores_disponiveis[8],
    "VGD": cores_disponiveis[9],
    "GTA": cores_disponiveis[10],
    "BLV": cores_disponiveis[11],
    "CFS": cores_disponiveis[12],
    "PLC": cores_disponiveis[13],
    "PDL": cores_disponiveis[14],
    "SRS": cores_disponiveis[15],
    "RTR": cores_disponiveis[16]
}

# Definir cor dos vértices de acordo com a comunidade
for vertice in grafo.vs:
    campus = vertice['campus']
    cor = cores_comunidades.get(campus, "gray")
    vertice["color"] = cor

# Detectar comunidades com base na conexão dos vértices
comunidades = grafo.community_multilevel(weights=None, return_levels=False)

# Definir visualização do grafo
visual_style = {
    "vertex_size": grafo.vs["size"],
    "layout": "fr",
    "bbox": (1600, 1600),
    "margin": 40,
    "edge_colors": grafo.es['color'],
    "edge_width": grafo.es['weight'],
    "vertex_label": grafo.vs["label"],
    "vertex_color": grafo.vs["color"],
    "mark_groups":True
}

plot(comunidades, "rede_com_comunidades.pdf", **visual_style)

plot(comunidades, "rede_com_comunidades_legenda.pdf", **visual_style, edge_label= grafo.es['weight'])

grafo.get_vertex_dataframe().to_csv('grafo_vertices.csv')
grafo.get_edge_dataframe().to_csv('grafo_arestas.csv')

# Criar um dicionário para mapear os índices dos vértices para os IDs dos grupos
indice_para_grupo = {i: vertice['name'] for i, vertice in enumerate(grafo.vs)}

# Create an empty list to store community data
communities_data = []

# Populate the list with community data
for i, community in enumerate(comunidades):
    cor_comunidade = visual_style['vertex_color'][community[0]]
    for indice_vertice in community:
        id_grupo = indice_para_grupo[indice_vertice]
        communities_data.append({'Comunidade': i, 'ID do Grupo': id_grupo, 'Cor da Comunidade': cor_comunidade})

# Convert the list of dictionaries into a DataFrame
df_comunidades = pd.DataFrame(communities_data)

# Save the DataFrame to a CSV file
df_comunidades.to_csv('comunidades.csv', index=False)
