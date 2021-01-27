import networkx as nx
import matplotlib.pyplot as plt
from HexGrid import *

def init_graph(hxgrid):

    G = nx.Graph()

    """Add nodes to graph"""
    for i in range(len(hxgrid.grid)):
        for j in range(len(hxgrid.grid[i])):
            G.add_node(int(hxgrid.grid[i][j].__str__()))

    """Add edges to graph"""

    neighbours = hxgrid.get_neighbours()

    for i in range(len(neighbours)):
        for j in range(len(neighbours[i])):
            G.add_edge(i, neighbours[i][j])
    
    return G

def find_positions(hxgrid):
    cell_pos = hxgrid.get_positions()
    nx_pos = {}
    for i in range(len(cell_pos)):
        nx_pos[i] = cell_pos[i]
    return nx_pos



t = Triangle(5, [(4,2)])

G = init_graph(t)
pos = find_positions(t)

nx.draw(G, pos, with_labels=True)
plt.show()













