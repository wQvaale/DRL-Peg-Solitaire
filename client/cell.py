class Cell:

    def __init__(self, x, y, cell_id=None, neighbours=[], empty=False):
        self.cell_id = cell_id
        self.x = x
        self.y = y 
        self.neighbours = neighbours
        self.empty = empty

    def getCellId(self):
        return self.cell_id

    def getPos(self):
        return (self.x, self.y)
    
    def setEmpty(self, empty):
        self.empty = empty