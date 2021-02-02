from cell import Cell



class Action:
    
    def __init__(self, a1, a2):
        self.jumper = a1
        self.jumpee = a2

    def stringify(self):
        return (self.jumper.cell_id, self.jumpee.cell_id)