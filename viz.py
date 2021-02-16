import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from hex_grid import Triangle, Diamond, HexGrid


def init_graph(board: HexGrid):
    """Initialize the NetworkX-Graph"""
    G = nx.Graph()

    # Add nodes to graph
    for i in range(len(board.grid)):
        for j in range(len(board.grid[i])):
            G.add_node(int(board.grid[i][j].getCellId()))

    # Add edges to graph
    neighbours = board.get_neighbours()
    for i in range(len(neighbours)):
        for j in range(len(neighbours[i])):
            G.add_edge(i, neighbours[i][j])

    return G


def find_node_positions(board: HexGrid, size: int):
    """ Finds the node positions based on board and size """

    cell_pos = []

    if board == Triangle:
        for i in range(size):
            for j in range(i + 1):
                cell_pos.append((j, size - i - 1))

    elif board == Diamond:
        for i in range(size):
            for j in range(size):
                cell_pos.append((j, size - i - 1))

    nx_pos = {}
    for i in range(len(cell_pos)):
        nx_pos[i] = cell_pos[i]
    return nx_pos


def find_node_colours(board: HexGrid, jumper=None, gets_jumped=None):
    """ Finds colours for a frame in video based on current state of grid """

    colour_map = []
    for row in board.grid:
        for cell in row:
            if jumper is None and gets_jumped is None:
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


def create_viz_grid(board: HexGrid):
    """ Create a new instance of board for viz """

    newHoles = []
    for h in board.holes:
        newHoles.append(h.getPos())

    if type(board) == Triangle:
        return Triangle(board.size, newHoles)
    elif type(board) == Diamond:
        return Diamond(board.size, newHoles)


class Viz:

    def __init__(self, board: HexGrid):
        """ Config for viz """
        self.fig, self.ax = plt.subplots()

        # Initialise Graph for viz
        self.G = init_graph(board)
        self.pos = find_node_positions(type(board), board.size)

        # Frames and all their corresponding HexGrid states
        self.frames = 1
        self.grid_states = []
        new_board = create_viz_grid(board)
        self.grid_states.append((new_board, None, None))

    def step(self, board, action):
        """ Save frame of action made by solver """
        self.frames += 1
        new_board = create_viz_grid(board)
        if action:
            jumper = action.jumper
            jumpee = action.jumpee
            self.grid_states.append((new_board, jumper, jumpee))
        else:
            self.grid_states.append((new_board, None, None))

    def update(self, i):
        """ Function that is used in FuncAnimation iteration """
        col = find_node_colours(self.grid_states[i][0], self.grid_states[i][1], self.grid_states[i][2])
        return nx.draw(self.G, pos=self.pos, node_color=col)

    def viz(self):
        """ Last step of visualising. Takes a figure and and update function to create video. """
        animation = FuncAnimation(self.fig, func=self.update, frames=self.frames, interval=500)
        plt.show()
