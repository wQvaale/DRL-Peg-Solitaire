import networkx as nx
from HexGrid import *

size = 5
t = Triangle(size, [(4,2)])
t.initialize_neighbours()

def initialise_graph(hexgrid):
    G = nx.Graph()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    neighbours = hexgrid.get_neighbours()
    for i in range(len(neighbours)):
        node_edges = []
        for j in range(len(neighbours[i])):
            node_edges.append((alphabet[i], neighbours[i][j]))
        G.add_edges_from(node_edges)
        print(node_edges)

initialise_graph(t)










