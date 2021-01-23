from cell import Cell


class HexGrid:

    def __init__(self):

        self.grid = []
        self.holes = []
        self.size


    def solitaire_jump(self, jumper, jumpee):
    #not sure how this will interact with the rest of the system but it is something
        #check if neighbours
        if jumper in jumpee.neighbours:
            #calculate hole
            y = jumper.y - jumpee.y
            x = jumper.x - jumpee.x
            #if calculated hole exists
            if 0 <= jumpee.y - y <= self.size and 0 <= jumpee.x - x <= self.size:
                hole = self.grid[jumpee.y - y][ jumpee.x - x]
                #if hole empty, perform jump
                if hole.empty and not jumper.empty and not jumpee.empty:
                    jumper.empty = True
                    jumpee.empty = True
                    hole.empty = False
                    self.holes.remove(hole)
                    self.holes.append(jumper)
                    self.holes.append(jumpee)
                    print(jumper, " jumped over ", jumpee, " to ", hole)
                else:
                    print("not legal")
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
        self.holes = []
        alphabet = "abcdefghijklmnopqrstuvwxyz" #alphabetical IDSsonly work for sizes up to 6
        ids = 0
        self.size = size
        for i in range(size):
            row = []
            for j in range(0,i+1):
                c = Cell(j,i,alphabet[ids], [], False)
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
    size = 4
    t = Triangle(size, [(3,2)])
    t.initialize_neighbours()
    t.vis()
    t.solitaire_jump((1,1),(3,1))
    t.vis()


