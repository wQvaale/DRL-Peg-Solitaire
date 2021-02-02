from HexGrid import Triangle
from randomAgent import RandomAgent, ActorCriticAgent
from Action import Action
import copy
import random

class SimWorld:

    def __init__(self, shape="Triangle", size=4, holes=[(1,1)]):
        if shape == "Triangle":
            self.board = Triangle(size, holes)

    def are_there_legal_moves(self):
        for hole in self.board.holes:
            for jumpee in hole.neighbours:
                for jumper in jumpee.neighbours:
                    y = jumper.y - jumpee.y
                    x = jumper.x - jumpee.x
                    if hole.y == jumpee.y - y and hole.x == jumpee.x - x:
                        #if hole empty, perform jump
                        if hole.empty and not jumper.empty and not jumpee.empty:
                            return True
        return False

    def get_all_legal_moves(self):
        moves = []
        for hole in self.board.holes:
            for jumpee in hole.neighbours:
                for jumper in jumpee.neighbours:
                    y = jumper.y - jumpee.y
                    x = jumper.x - jumpee.x
                    if hole.y == jumpee.y - y and hole.x == jumpee.x - x:
                        #if hole empty, perform jump
                        if hole.empty and not jumper.empty and not jumpee.empty:
                            moves.append(Action(jumper, jumpee))
        return moves



    def is_victory(self):
        num_cells = self.board.size*(self.board.size+1)/2
        if len(self.board.holes) == num_cells - 1:
            return True
    
    def solitaire_jump(self, jumper, jumpee):
        #not sure how this will interact with the rest of the system but it is something
            #check if neighbours
            if jumper in jumpee.neighbours:
                #calculate hole
                y = jumper.y - jumpee.y
                x = jumper.x - jumpee.x
                #if calculated hole exists - > is within the boundaries of the triangle
                if 0 <= jumpee.y - y < self.board.size and 0 <= jumpee.x - x <= jumpee.y - y:
                    hole = self.board.grid[jumpee.y - y][ jumpee.x - x]
                    #if hole empty, perform jump
                    if hole.empty and not jumper.empty and not jumpee.empty:
                        jumper.empty = True
                        jumpee.empty = True
                        hole.empty = False
                        self.board.holes.remove(hole)
                        self.board.holes.append(jumper)
                        self.board.holes.append(jumpee)
                        #print(jumper, " jumped over ", jumpee, " to ", hole)
                    else:
                        print("not legal")
                else:
                    print("not legal")
            else:
                print("not legal")

    def play_solitaire_random_agent(self):
        A = RandomAgent()
        self.board.vis()
        while True:

        
            #gets cell IDs from agent
            jumper, jumpee = A.getMove(self.get_all_legal_moves())
            #finds corresponding cells for the IDs
            for row in range(len(self.board.grid)):
                for col in range(row+1):
                    if self.board.grid[row][col].cell_id == jumper:
                        jumper = self.board.grid[row][col]
                    if self.board.grid[row][col].cell_id == jumpee:
                        jumpee = self.board.grid[row][col]

            #plays move
            self.solitaire_jump(jumper, jumpee)
            self.board.vis()
            
            if self.is_victory():
                print("congrats")
                break
            elif not self.are_there_legal_moves():
                print("u suck")
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
            elif not self.are_there_legal_moves():
                print("u suck")
                break
            

def train_agent():        
        
    a = ActorCriticAgent()

    for i in range(1000):
        if i % 100 == 0:
            print(i)
        x = random.randint(0,3)
        y = random.randint(0, x)

        s = SimWorld(size=4, holes=[(y,x)])
        s.play_RL(a, 0.5)
        a.flush()
        
    aw = a.wins
    but= len(a.actor.state_action_pairs)

    for i in range(10) :
        x = random.randint(0,3)
        y = random.randint(0, x)

        s = SimWorld(size=4, holes=[(2,2)])
        s.play_RL(a, greed=0, vis=True, choose_best=True)
        a.flush()

    print(a.actor.state_action_pairs)
    print(aw, a.wins-aw)
    print(but, len(a.actor.state_action_pairs))

train_agent()