import copy
import random
from Action import Action
from Viz import Viz, create_Viz_Grid
from HexGrid import Triangle, Diamond
from randomAgent import RandomAgent, ActorCriticAgent

class SimWorld:

    def __init__(self, shape, size=4, holes=[(1,1)]):

        if shape == "Triangle":
            self.board = Triangle(size, holes)
            self.num_cells = self.board.size*(self.board.size+1)/2 

        elif shape == "Diamond":
            self.board = Diamond(size, holes)
            self.num_cells = self.board.size*self.board.size
        
        self.viz = Viz(self.board)

    def get_all_legal_moves(self):

        """ Returns all possible moves given board state """

        legal_moves = []

        for hole in self.board.holes:
            for gets_jumped in hole.neighbours:
                for jumper in gets_jumped.neighbours:
                    
                    x_diff = jumper.x - gets_jumped.x
                    y_diff = jumper.y - gets_jumped.y

                    """ Check if jumper and gets_jumped aligned with hole """
                    if hole.x == gets_jumped.x - x_diff and hole.y == gets_jumped.y - y_diff:
                        if hole.empty and not jumper.empty and not gets_jumped.empty:
                            legal_moves.append((hole, jumper, gets_jumped))

        return legal_moves

    def is_victory(self):
        if len(self.board.holes) == self.num_cells-1:
            return True
    
    def solitaire_jump(self, hole, jumper, gets_jumped):

        self.viz.step(create_Viz_Grid(self.board), jumper, gets_jumped)

        """ Update empty """
        jumper.empty = True
        gets_jumped.empty = True
        hole.empty = False

        """ Update holes """
        self.board.holes.remove(hole)   
        self.board.holes.append(jumper)
        self.board.holes.append(gets_jumped)

        self.viz.step(create_Viz_Grid(self.board), None, None)
        print(jumper.getCellId(), " jumped over ", gets_jumped.getCellId(), " to ", hole.getCellId())

    def play_solitaire_random_agent(self):
        
        """ Plays game of solitiare with random agent """
        
        self.viz.step(create_Viz_Grid(self.board), None, None)
        A = RandomAgent()
        while True:
            
            """ Get all legal moves and do jump """
            hole, jumper, gets_jumped = A.getMove(self.get_all_legal_moves())
            self.solitaire_jump(hole, jumper, gets_jumped)
            
            if self.is_victory():
                self.board.vis()
                print("congrats")
                self.viz.viz()
                break
            elif len(self.get_all_legal_moves()) == 0:
                self.board.vis()
                print("u suck")
                self.viz.viz()
                break
    
    def play_RL(self, agent, greed=0, vis=False, choose_best=False):
        if vis:
            self.board.vis()
        if self.are_there_legal_moves():
            while True:
                #gets cell IDs from agent
                prev_state = self.board.stringify()
                action = agent.get_move(prev_state, moves=self.get_all_legal_moves(), choose_best=choose_best)
                jumper = action.jumper
                jumpee = action.jumpee

                #plays move
                self.solitaire_jump(jumper, jumpee)
                if vis:
                    self.board.vis()
                
                if self.is_victory():
                    agent.update(prev_state, action, 1, self.board.stringify())
                    agent.wins += 1
                    break
                elif not self.are_there_legal_moves():
                    agent.update(prev_state, action, 0, self.board.stringify())
                    break
                else:
                    agent.update(prev_state, action, 0, self.board.stringify())

    def play_solitaire_human_terminal(self):
        self.board.vis()
        while True:
         
            inp = input("move")
            jumper = int(inp[0])
            jumpee = int(inp[1])

            for row in range(len(self.board.grid)):
                for col in range(row+1):
                    print(self.board.grid[row][col].cell_id)
                    if self.board.grid[row][col].cell_id == jumper:
                        jumper = self.board.grid[row][col]
                    if self.board.grid[row][col].cell_id == jumpee:
                        jumpee = self.board.grid[row][col]
            self.solitaire_jump(jumper, jumpee)
            self.board.vis()
            
            if self.is_victory():
                print("congrats")
                break
            elif len(self.get_all_legal_moves()) == 0:
                print("u suck")
                break
            

def train_agent():        
        
    a = ActorCriticAgent()
    for row in range(0, 5):
        for col in range(row):

            for i in range(1000):
                if i % 100 == 0:
                    print(i)
            
                s = SimWorld(size=5, holes=[(row,col)])
                s.play_RL(a, 0.5)
                a.flush()
            
    aw = a.wins
    but= len(a.actor.state_action_pairs)

    for i in range(10) :
        x = random.randint(0,4)
        y = random.randint(0, x)

        s = SimWorld(size=5, holes=[(y,x)])
        s.play_RL(a, greed=0, vis=True, choose_best=True)
        a.flush()

    print(a.actor.state_action_pairs)
    print(aw, a.wins-aw)
    print(but, len(a.actor.state_action_pairs))

train_agent()
    

s = SimWorld(shape="Triangle")
s.play_solitaire_random_agent()
