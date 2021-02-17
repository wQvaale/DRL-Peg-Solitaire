class Cell:

    def __init__(self, x, y, cell_id=None, neighbours=[], empty=False):
        self.cell_id = cell_id
        self.x = x
        self.y = y
        self.neighbours = neighbours
        self.empty = empty

    def get_cell_id(self):
        return self.cell_id

    def get_pos(self):
        return (self.x, self.y)

    def set_empty(self, empty):
        self.empty = empty
