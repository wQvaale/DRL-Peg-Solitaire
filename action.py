from cell import Cell


class Action:

    def __init__(self, jumper, jumpee, hole):
        self.jumper = jumper
        self.jumpee = jumpee
        self.hole = hole

    def stringify(self):
        return self.jumper.cell_id, self.jumpee.cell_id