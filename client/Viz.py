import networkx as nx
import matplotlib.pyplot as plt
from HexGrid import *

def init_graph(shape):

    G = nx.Graph()

    """Add nodes to graph"""
    for i in range(len(shape.grid)):
        for j in range(len(shape.grid[i])):
            G.add_node(int(shape.grid[i][j].__str__()))

    """Add edges to graph"""

    neighbours = shape.get_neighbours()

    for i in range(len(neighbours)):
        for j in range(len(neighbours[i])):
            G.add_edge(i, neighbours[i][j])
    
    return G

t = Triangle(5, [(4,2)])

G = init_graph(t)

print(G.nodes())
print(G.edges())

nx.draw(G)
plt.show()













