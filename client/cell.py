class Cell:

    def __init__(self, x, y, cell_id=None, neighbours=[], empty=False):
        self.cell_id = cell_id
        self.x = x
        self.y = y 
        self.neighbours = neighbours
        self.empty = empty

        
    #def __str__(self):
    #    return str(self.cell_id)

    def getCellId(self):
        return self.cell_id

    def getPos(self):
        return (self.x, self.y)
    
    def setPos(self, x, y):
        self.x = x
        self.y = y

        