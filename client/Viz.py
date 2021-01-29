import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from HexGrid import *
from cell import Cell

def init_graph(hxgrid):

    G = nx.Graph()

    """Add nodes to graph"""

    for i in range(len(hxgrid.grid)):
        for j in range(len(hxgrid.grid[i])):
            G.add_node(int(hxgrid.grid[i][j].getCellId()))

    """Add edges to graph"""

    neighbours = hxgrid.get_neighbours()

    for i in range(len(neighbours)):
        for j in range(len(neighbours[i])):
            G.add_edge(i, neighbours[i][j])

    return G

def find_node_positions(shape, size):

    """ Finds the node positions based on shape and size """

    cell_pos = []

    if shape == Triangle:
        for i in range(size):
            for j in range(i+1):
                cell_pos.append((j, size-i-1))

    elif shape == Diamond:
        for i in range(size):
            for j in range(size):
                cell_pos.append((j, size-i-1))

    nx_pos = {}
    for i in range(len(cell_pos)):
        nx_pos[i] = cell_pos[i]
    return nx_pos

def find_node_colours(hxgrid, jumper=None, gets_jumped=None):

    """ Finds colours for a frame in video based on current state of grid """

    colour_map = []
    for row in hxgrid.grid:
        for cell in row:
            if jumper == None and gets_jumped == None:
                if cell.empty:
                    colour_map.append('lightgrey')
                else: 
                    colour_map.append('black')
            else:
                if cell.x == jumper.x and cell.y == jumper.y:
                    colour_map.append('green')
                elif cell.x == gets_jumped.x and cell.y == gets_jumped.y:
                    colour_map.append('red')
                elif cell.empty:
                    colour_map.append('lightgrey')
                else: 
                    colour_map.append('black')

    return colour_map

def create_Viz_Grid(hxgrid):

    """ Create a new instance of hxgrid for viz """

    newHoles = []
    for h in hxgrid.holes:
        newHoles.append(h.getPos())

    if type(hxgrid) == Triangle:
        newHx = Triangle(hxgrid.size, newHoles)
    elif type(hxgrid) == Diamond:
        newHx = Diamond(hxgrid.size, newHoles)
    return newHx

class Viz:

    def __init__(self, hxgrid):

        """ Config for viz """
        self.fig, self.ax = plt.subplots()

        """ Initialise Graph for viz """
        self.G = init_graph(hxgrid)
        self.pos = find_node_positions(type(hxgrid), hxgrid.size)

        """ Frames and all their corresponding HexGrid states """
        self.frames = 1
        self.grid_states = []
        newHx = create_Viz_Grid(hxgrid)
        self.grid_states.append((newHx, None, None))

    def step(self, hxgrid, jumper=None, gets_jumped=None):

        """ Save frame of action made by solver """
        self.frames += 1
        self.grid_states.append((hxgrid, jumper, gets_jumped))

    def update(self, i):

        """ Function that is used in FuncAnimation iteration """
        col = find_node_colours(self.grid_states[i][0], self.grid_states[i][1], self.grid_states[i][2])
        return nx.draw(self.G, pos=self.pos, node_color=col)

    def viz(self):

        """ Last step of visualising. Takes a figure and and update function to create video. """

        animation = FuncAnimation(self.fig, func=self.update, frames=self.frames, interval=500)
        plt.show()