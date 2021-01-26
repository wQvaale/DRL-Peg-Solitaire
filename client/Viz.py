import networkx as nx
import matplotlib.pyplot as plt
from HexGrid import *

def init_graph():
    return nx.Graph()

def add_nodes(G, grid):

    """Add nodes to graph"""

    for i in range(len(grid.grid)):
        for j in range(len(grid.grid[i])):
            G.add_node(grid.grid[i][j].__str__())
    return G

def add_edges(G, grid):

    alphabet = "abcdefghijklmnopqrstuvwxyz"
    neighbours = grid.get_neighbours()

    """Add edges to graph"""

    for i in range(len(neighbours)):
        node_edges = []
        for j in range(len(neighbours[i])):
            node_edges.append((alphabet[i], neighbours[i][j]))
        G.add_edges_from(node_edges)
    return G

t = Triangle(5, [(4,2)])
t.initialize_neighbours()

G = init_graph()
G = add_nodes(G, t)
G = add_edges(G, t)

print(G.nodes())
print(G.edges())

nx.draw(G)
plt.show()













