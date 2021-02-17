from hex_grid import Triangle, Diamond
from action import Action


class SimWorld:

    def __init__(self, cfg):
        """ Initialize the SimulationWorld and the game state """
        self.cfg = cfg
        self.board = None
        self.num_cells = None
        self.reset_world()

    def reset_world(self):
        if self.cfg.shape.upper() == "TRIANGLE":
            self.board = Triangle(self.cfg.size, self.cfg.holes)
            self.num_cells = self.board.size * (self.board.size + 1) / 2
        elif self.cfg.shape.upper() == "DIAMOND":
            self.board = Diamond(self.cfg.size, self.cfg.holes)
            self.num_cells = self.board.size * self.board.size
        else:
            raise Exception("Shape must be 'Triangle' or 'Diamond'")

    def get_all_legal_moves(self):
        """ Returns all possible moves given board state """
        legal_moves = []

        for hole in self.board.holes:
            for jumpee in hole.neighbours:
                for jumper in jumpee.neighbours:

                    x_diff = jumper.x - jumpee.x
                    y_diff = jumper.y - jumpee.y

                    # Check if jumper and jumpee aligned with hole
                    if hole.x == jumpee.x - x_diff and hole.y == jumpee.y - y_diff:
                        if hole.empty and not jumper.empty and not jumpee.empty:
                            legal_moves.append(Action(jumper, jumpee, hole))

        return legal_moves

    def is_victory(self):
        if len(self.board.holes) == self.num_cells - 1:
            return True

    def is_loss(self):
        return not self.get_all_legal_moves()

    def solitaire_jump(self, action: Action):
        jumper = action.jumper
        jumpee = action.jumpee
        hole = action.hole

        """ Update empty """
        jumper.empty = True
        jumpee.empty = True
        hole.empty = False

        """ Update holes """
        self.board.holes.remove(hole)
        self.board.holes.append(jumper)
        self.board.holes.append(jumpee)

    def get_remaining_pegs(self):
        return self.num_cells - len(self.board.holes)

    def get_reward(self):
        reward = 0
        if self.is_victory():
            reward = self.board.size
        elif self.is_loss():
            reward = -1 * self.get_remaining_pegs()
        return reward
