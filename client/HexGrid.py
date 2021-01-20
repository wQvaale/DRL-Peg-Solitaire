from cell import Cell


class HexGrid:

    def __init__(self):
        pass


class Diamond(HexGrid):

    def __init__(self):
        pass


class Triangle(HexGrid):

    def __init__(self, size):
        cells = []
        alphabet = "abcdefghijklmnopqrstuvwxyz" #alphabetical IDSsonly work for sizes up to 6
        ids = 0
        for i in range(size):
            row = []
            for j in range(0,i+1):
                c = Cell(alphabet[ids], [], False)
                row.append(c)
                ids += 1
            cells.append(row)

        self.grid = cells

    def vis(self):
        for r in self.grid:
            for x in r:
                n = [c.cell_id for c in x.neighbours]
                print(x.cell_id, "Neighbours: ", [c.cell_id for c in x.neighbours])
    
    def initialize_neighbours(self):
        #pattern = [(0, 1),(1, 1),(1, 0),(0, -1),(-1, -1),(-1, 0)]
        for r in range(len(self.grid)):
            for c in range(len(self.grid[r])):
                #epic use of try
                try:
                    self.grid[r][c].neighbours.append(self.grid[r][c+1])
                except Exception as e:
                    print(e)
                try:
                    self.grid[r][c].neighbours.append(self.grid[r+1][c])
                except:
                    print("woops")
                try:
                    self.grid[r][c].neighbours.append(self.grid[r+1][c+1])
                except:
                    print("woops")
                try:
                    if c > 0:
                        self.grid[r][c].neighbours.append(self.grid[r][c-1])
                except:
                    print("woops")
                try:
                    if r > 0:
                        self.grid[r][c].neighbours.append(self.grid[r-1][c])
                except:
                    print("woops")
                try:
                    if c > 0 and r > 0:
                        self.grid[r][c].neighbours.append(self.grid[r-1][c-1])
                except:
                    print("woops")



def example_use_of_triangle():
    size = 4

    t = Triangle(size)
    t.initialize_neighbours()
    t.vis()

