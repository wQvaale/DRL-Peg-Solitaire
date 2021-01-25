class Cell:

    def __init__(self, x, y, cell_id=None, neighbours=[], empty=False):
        self.cell_id = cell_id
        self.x = x
        self.y = y 
        self.neighbours = neighbours
        self.empty = empty

        
    def __str__(self):
        return str(self.cell_id)
        