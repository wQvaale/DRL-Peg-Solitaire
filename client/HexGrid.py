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


class Diamond(HexGrid):

    def __init__(self):
        pass


class Triangle(HexGrid):


    def __init__(self, size, empties=[]):

        cells = []
        self.holes = []
        ids = 0
        self.size = size
        for i in range(size):
            row = []
            for j in range(0,i+1):
                c = Cell(j, i, ids, [], False)
                if (i,j) in empties:
                    c.empty = True
                    self.holes.append(c)

                row.append(c)
                ids += 1
            cells.append(row)


        self.grid = cells
        self.initialize_neighbours()

    def vis(self):
        for r in self.grid:
            for x in r:
                print(x.cell_id, x.empty,  "Neighbours: ", [c.cell_id for c in x.neighbours])

    
    def initialize_neighbours(self):
        #pattern = [(0, 1),(1, 1),(1, 0),(0, -1),(-1, -1),(-1, 0)]
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                #epic use of try
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


def example_use_of_triangle():
    size = 5
    t = Triangle(size, [(4,2)])



