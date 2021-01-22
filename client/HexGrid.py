from cell import Cell


class HexGrid:

    def __init__(self):
        self.grid = []

    def solitaire_jump(self, jumper, jumpee):
    #not sure how this will interact with the rest of the system but it is something

        #check if neighbours
        if self.grid[jumper[0]][jumper[1]] in self.grid[jumpee[0]][jumpee[1]].neighbours:

            #calculate hole
            y = jumper[0] - jumpee[0]
            x = jumper[1] - jumpee[1]
            hole = (jumpee[0] - y, jumpee[1] - x)

            #if hole empty, perform jump
            if self.grid[hole[0]][hole[1]].empty:
                self.grid[jumper[0]][jumper[1]].empty = True
                self.grid[jumpee[0]][jumpee[1]].empty = True
                self.grid[hole[0]][hole[1]].empty = False
                print(jumper, " jumped over ", jumpee, " to ", hole)
            else:
                print("not legal")
        else:
            print("not legal")


class Diamond(HexGrid):

    def __init__(self):
        pass


class Triangle(HexGrid):

    def __init__(self, size, empties=[]):
        cells = []
        alphabet = "abcdefghijklmnopqrstuvwxyz" #alphabetical IDSsonly work for sizes up to 6
        ids = 0
        for i in range(size):
            row = []
            for j in range(0,i+1):
                c = Cell(alphabet[ids], [], ((i,j) in empties))
                row.append(c)
                ids += 1
            cells.append(row)

        self.grid = cells

    def vis(self):
        for r in self.grid:
            for x in r:
                n = [c.cell_id for c in x.neighbours]
                print(x.cell_id, x.empty,  "Neighbours: ", [c.cell_id for c in x.neighbours])
    
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
    size = 5
    t = Triangle(size, [(4,2)])
    t.initialize_neighbours()
    t.vis()
    t.solitaire_jump((1,1),(3,1))
    t.vis()

example_use_of_triangle()