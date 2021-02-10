from viz import Viz
from hex_grid import Triangle, Diamond
from agent import RandomAgent
from action import Action


class SimWorld:

    def __init__(self, shape, size=4, holes=None, viz_toggle=False):
        self.viz_toggle = viz_toggle
        if holes is None:
            holes = [(1, 1)]

        if shape.upper() == "TRIANGLE":
            self.board = Triangle(size, holes)
            self.num_cells = self.board.size * (self.board.size + 1) / 2

        elif shape.upper() == "DIAMOND":
            self.board = Diamond(size, holes)
            self.num_cells = self.board.size * self.board.size

        if viz_toggle:
            self.viz = Viz(self.board)

    def get_all_legal_moves(self):
        """ Returns all possible moves given board state """
        legal_moves = []

        for hole in self.board.holes:
            for gets_jumped in hole.neighbours:
                for jumper in gets_jumped.neighbours:

                    x_diff = jumper.x - gets_jumped.x
                    y_diff = jumper.y - gets_jumped.y

                    # Check if jumper and gets_jumped aligned with hole
                    if hole.x == gets_jumped.x - x_diff and hole.y == gets_jumped.y - y_diff:
                        if hole.empty and not jumper.empty and not gets_jumped.empty:
                            legal_moves.append(Action(jumper, gets_jumped, hole))

        return legal_moves

    def is_victory(self):
        if len(self.board.holes) == self.num_cells - 1:
            return True

    def solitaire_jump(self, action: Action):
        if self.viz_toggle:
            self.viz.step(self.board, action)

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

        if self.viz_toggle:
            self.viz.step(self.board, None)

    def play_solitaire_random_agent(self):

        """ Plays game of solitiare with random agent """

        # TODO: DON't do this unless enabled / toggled
        # self.viz.step(self.board, None, None)
        A = RandomAgent()
        while True:

            """ Get all legal moves and do jump """
            action = A.get_move(self.get_all_legal_moves())

            self.solitaire_jump(action)

            if self.is_victory():
                self.board.vis()
                self.viz.viz()
                break
            elif len(self.get_all_legal_moves()) == 0:
                self.board.vis()
                self.viz.viz()
                break

    def play_RL(self, agent, greed=0, vis=False, choose_best=False):
        if vis:
            self.board.vis()
        if self.get_all_legal_moves():
            while True:
                # gets cell IDs from agent
                prev_state = self.board.stringify()
                action = agent.get_move(prev_state, moves=self.get_all_legal_moves(), choose_best=choose_best)

                # plays move
                self.solitaire_jump(action)
                if vis:
                    self.board.vis()

                if self.is_victory():
                    agent.update(prev_state, action, 1, self.board.stringify())
                    agent.wins += 1
                    if self.viz_toggle:
                        self.board.vis()
                        self.viz.viz()
                    break
                elif not self.get_all_legal_moves():
                    agent.update(prev_state, action, 0, self.board.stringify())
                    if self.viz_toggle:
                        self.board.vis()
                        self.viz.viz()
                    break
                else:
                    agent.update(prev_state, action, 0, self.board.stringify())
