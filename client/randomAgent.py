from HexGrid import Triangle
from collections import defaultdict
from Action import Action
import random


INITIAL_PI_RANGE = (1,10)
DIVIDER = 100
LEARNING_RATE = 0.2
DISCOUNT = 0.9
DECAY = 0.1

class RandomAgent:
    def getMove(self, moves):
        return random.choice(moves)


class Critic:

    def __init__(self):
        self.state_value = defaultdict(lambda: 0) 
        self.eligibility = defaultdict(lambda: 0) 

class Actor:

    def __init__(self):
        self.state_action_pairs = defaultdict(lambda: 0) 
        self.eligibility = defaultdict(lambda: 0) 
        

class ActorCriticAgent:
    def __init__(self):
        self.critic = Critic()
        self.actor = Actor()
        self.episode = []
        self.wins=0


    def flush(self):
        self.actor.eligibility={}
        self.critic.eligibility={}
        self.episode=[]
        
        
    
    def update(self, state, action, reward, new_state): 
        self.episode.append((state, action.stringify()))
        self.set_eligibility(state, action)
           
        gamma = reward + DISCOUNT * (self.critic.state_value[new_state] - self.critic.state_value[state])
        for (state, action) in self.episode:
           
            self.critic.state_value[state] = self.critic.state_value[state] + LEARNING_RATE* gamma*self.critic.eligibility[state]
            self.critic.eligibility[state] = DISCOUNT * DECAY * self.critic.eligibility[state]
            self.actor.state_action_pairs[(state, action)] = self.actor.state_action_pairs[(state, action)] + LEARNING_RATE * gamma * self.actor.eligibility[(state,action)]

            self.actor.eligibility[(state, action)] = DISCOUNT * DECAY * self.actor.eligibility[(state,action)]

    

    def get_move(self, state, moves, e_greedy=0.3, choose_best=False):
        best = None

        for action in moves:
            
            a = action.stringify()
            print((state, a), self.actor.state_action_pairs[(state, a)])
            if best == None or best[2] < self.actor.state_action_pairs[(state, a)]:
                best = (state, action ,self.actor.state_action_pairs[(state, a)])

        if random.random() < e_greedy or choose_best:
            m = best[1]

            print("best")
        else:
            m = random.choice(moves)
            print("random")
        return m

    def set_eligibility(self, state,action):
        self.actor.eligibility[(state, action.stringify())] = 1
        self.critic.eligibility[(state)] = 1

