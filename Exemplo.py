from igraph import *

grafo = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])

grafo.vs["name"] = ["Guilherme", "Adam", "Andre", "João", "Gabriela", "Julia", "Flavia"]
grafo.vs["age"] = [20, 32, 35, 29, 21, 22, 40]
grafo.vs["gender"] = ["m", "m", "m", "m", "f", "f", "f"]
grafo.es["is_formal"] = [False, False, True, True, False, True, False]

color_dict = {"m": "blue", "f": "pink"}

visual_style = {
    "vertex_size": 10,
    "vertex_color": [color_dict[gender] for gender in grafo.vs["gender"]],
    "vertex_label": grafo.vs["name"],
    "edge_width": [1 + 2 * int(is_formal) for is_formal in grafo.es["is_formal"]],
    "layout": "kk",
    "bbox": (300, 300),
    "margin": 20,
    "vertex_label_dist": 2
}

layout = grafo.layout("kk")
plot(grafo, layout = layout)
# plot(g, layout=layout, vertex_color=[color_dict[gender] for gender in g.vs["gender"]])
plot(grafo, "Rede_IMG_COMUNIDADES_3VESPERTINO.pdf", **visual_style)