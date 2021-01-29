from cell import Cell


class HexGrid:

    def __init__(self):

        self.grid = []
        self.holes = []
        self.size

    def get_neighbours(self):

        """ Returns list of cell neighbours"""
        neighbours = []
        for r in self.grid:
            for x in r:
                neighbours.append([c.cell_id for c in x.neighbours])
        return neighbours
    
    def initialize_neighbours(self):
        
        """ For each cell, try to add a neighbour. Possible if node exist. """
        """ pattern = [(0, 1),(1, 1),(1, 0),(0, -1),(-1, -1),(-1, 0)] """

        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                try:
                    self.grid[r][c].neighbours.append(self.grid[r][c+1])
                except:
                    None
                try:
                    self.grid[r][c].neighbours.append(self.grid[r+1][c])
                except:
                    None
                try:
                    self.grid[r][c].neighbours.append(self.grid[r+1][c+1])
                except:
                    None
                try:
                    if c > 0:
                        self.grid[r][c].neighbours.append(self.grid[r][c-1])
                except:
                    None
                try:
                    if r > 0:
                        self.grid[r][c].neighbours.append(self.grid[r-1][c])
                except:
                    None
                try:
                    if c > 0 and r > 0:
                        self.grid[r][c].neighbours.append(self.grid[r-1][c-1])
                except:
                    None
    
    def vis(self):

        """ Print all nodes with empty and corresponding neighbours """

        for r in self.grid:
            for x in r:
                print(x.cell_id, x.empty,  "Neighbours: ", [c.cell_id for c in x.neighbours])


class Diamond(HexGrid):

    def __init__(self, size, empties=[]):

        """ Initialise Diamond shaped Hexgrid """
        
        self.size = size
        self.holes = []

        cells = []
        ids = 0
        for i in range(size):
            row = []
            for j in range(size):
                c = Cell(j, i, ids, [], False)
                if (j, i) in empties:
                    c.empty = True
                    self.holes.append(c)
                row.append(c)
                ids += 1
            cells.append(row)
        
        self.grid = cells
        self.initialize_neighbours()


class Triangle(HexGrid):


    def __init__(self, size, empties=[]):

        """ Initialise Triangle shaped Hexgrid """

        self.size = size
        self.holes = []
        
        cells = []
        ids = 0
        for i in range(size):
            row = []
            for j in range(0,i+1):
                c = Cell(j, i, ids, [], False)
                if (j, i) in empties:
                    c.empty = True
                    self.holes.append(c)
                row.append(c)
                ids += 1
            cells.append(row)

        self.grid = cells
        self.initialize_neighbours()


def example():
    size = 3
    t = Diamond(size, [(1,0)])
    t.vis()

example()

