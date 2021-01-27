import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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

def find_node_positions(hxgrid):
    cell_pos = hxgrid.get_positions()
    nx_pos = {}
    for i in range(len(cell_pos)):
        nx_pos[i] = cell_pos[i]
    return nx_pos

def find_node_colours(hxgrid):
    colour_map = []
    for row in hxgrid.grid:
        for cell in row:
            if cell.empty:
                colour_map.append('lightgrey')
            else:
                colour_map.append('skyblue')
    return colour_map

class Viz:

    def __init__(self, hxgrid):
        self.fig, self.ax = plt.subplots()
        self.frames = 1
        self.hexgrid = hxgrid
        self.G = init_graph(hxgrid)
        self.pos = find_node_positions(hxgrid)
        self.init_node_col = find_node_colours(hxgrid)
        nx.draw(self.G, pos=self.pos, node_color=self.init_node_col)

    def steps(self):
        self.frames += 1

    def update(self, i):
        col = find_node_colours(self.hexgrid)
        return nx.draw(self.G, pos=self.pos, node_color=col)


    def viz(self):
        animation = FuncAnimation(self.fig, func=self.update, frames=self.frames, interval=200)
        plt.show()

t = Triangle(5, [(4,2)])
v = Viz(t)
for i in range(len(t.grid)):
    v.steps()
v.viz()






