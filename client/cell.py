class Cell:

    def __init__(self, cell_id=None, neighbours=[], empty=False):
        self.cell_id = cell_id
        self.neighbours = neighbours
        self.empty = empty

        
    def __str__(self):
        return self.cell_id
        