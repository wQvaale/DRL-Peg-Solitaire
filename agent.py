import random
from config import Config
from collections import defaultdict
import torch


class RandomAgent:
    @staticmethod
    def get_move(moves):
        return random.choice(moves)


class Critic:

    def __init__(self):
        self.state_value = defaultdict(lambda: 0)
        self.eligibility = defaultdict(lambda: 0)

class NeuralCritic(torch.nn.Module):

    def __init__(self, layers=4 ,sizes=[16, 8, 1]):
        self.layers = []
        for i in range(len(sizes)-1):
            self.layers.append(torch.rand(sizes[i],sizes[i+1]))
        self.eligibility = defaultdict(lambda: 0)
    
    def forward(self, X):
        self.z = torch.matmul(X, self.layers[0]) 
        self.z = self.sigmoid(self.z) # activation function
        for layer in self.layers[1:]:
            self.z = torch.matmul(self.z, layer) 
            self.z = self.sigmoid(self.z)
        return self.z
        
    def sigmoid(self, s):
        return 1 / (1 + torch.exp(-s))
    
    def sigmoidPrime(self, s):
        # derivative of sigmoid
        return s * (1 - s)
    
    def backward(self, X, y, o):
        self.o_error = y - o # error in output
        self.o_delta = self.o_error * self.sigmoidPrime(o) # derivative of sig to error
        self.z2_error = torch.matmul(self.o_delta, torch.t(self.W2))
        self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)
        self.W1 += torch.matmul(torch.t(X), self.z2_delta)
        self.W2 += torch.matmul(torch.t(self.z2), self.o_delta)
        
    def train(self, X, y):
        # forward + backward pass for training
        o = self.forward(X)
        self.backward(X, y, o)
        
    def saveWeights(self, model):
        # we will use the PyTorch internal storage functions
        torch.save(model, "NN")
        # you can reload model with all the weights and so forth with:
        # torch.load("NN")
        
    def predict(self):
        print ("Predicted data based on trained weights: ")
        print ("Input (scaled): \n" + str(xPredicted))
        print ("Output: \n" + str(self.forward(xPredicted)))





class Actor:

    def __init__(self):
        self.state_action_pairs = defaultdict(lambda: 0)
        self.eligibility = defaultdict(lambda: 0)


class ActorCriticAgent:
    def __init__(self, cfg: Config):
        self.critic = Critic()
        self.actor = Actor()
        self.episode = []
        self.wins = 0
        self.cfg = cfg

    def flush(self):
        self.actor.eligibility = defaultdict(lambda: 0)
        self.critic.eligibility = defaultdict(lambda: 0)
        self.episode = []

    def update(self, state, action, reward, new_state):
        self.episode.append((state, action.stringify()))
        self.set_eligibility(state, action)
        # print("CriticValue:\t",self.critic.state_value)

        gamma = reward + self.cfg.discount * (self.critic.state_value[new_state] - self.critic.state_value[state])

        for (state, action) in self.episode:
            self.critic.state_value[state] = self.critic.state_value[state] + self.cfg.learning_rate * gamma * \
                                             self.critic.eligibility[state]
            self.critic.eligibility[state] = self.cfg.discount * self.cfg.decay * self.critic.eligibility[state]
            self.actor.state_action_pairs[(state, action)] = self.actor.state_action_pairs[
                                                                 (state, action)] + self.cfg.learning_rate * gamma * \
                                                             self.actor.eligibility[(state, action)]

            self.actor.eligibility[(state, action)] = self.cfg.discount * self.cfg.decay * self.actor.eligibility[(state, action)]

    def get_move(self, state, moves, e_greedy=0.3, choose_best=False):
        best = None

        for action in moves:
            a = action.stringify()
            if best is None or best[2] < self.actor.state_action_pairs[(state, a)]:
                best = (state, action, self.actor.state_action_pairs[(state, a)])

        if random.random() < e_greedy or choose_best:
            m = best[1]
        else:
            m = random.choice(moves)
        return m

    def set_eligibility(self, state, action):
        self.actor.eligibility[(state, action.stringify())] = 1
        self.critic.eligibility[state] = 1



class NeuralAgent:
    def __init__(self, cfg: Config):
        self.critic = NeuralCritic()
        self.actor = Actor()
        self.episode = []
        self.wins = 0
        self.cfg = cfg

    def flush(self):
        self.actor.eligibility = defaultdict(lambda: 0)
        self.critic.eligibility = defaultdict(lambda: 0)
        self.episode = []

    def update(self, state, action, reward, new_state):
        self.episode.append((state, action.stringify()))
        self.set_eligibility(state, action)
        # print("CriticValue:\t",self.critic.state_value)

        gamma = reward + self.cfg.discount * (self.critic.state_value[new_state] - self.critic.state_value[state])

        for (state, action) in self.episode:
            self.critic.state_value[state] = self.critic.state_value[state] + self.cfg.learning_rate * gamma * \
                                             self.critic.eligibility[state]
            self.critic.eligibility[state] = self.cfg.discount * self.cfg.decay * self.critic.eligibility[state]
            self.actor.state_action_pairs[(state, action)] = self.actor.state_action_pairs[
                                                                 (state, action)] + self.cfg.learning_rate * gamma * \
                                                             self.actor.eligibility[(state, action)]

            self.actor.eligibility[(state, action)] = self.cfg.discount * self.cfg.decay * self.actor.eligibility[(state, action)]

    def get_move(self, state, moves, e_greedy=0.3, choose_best=False):
        best = None

        for action in moves:
            a = action.stringify()
            if best is None or best[2] < self.actor.state_action_pairs[(state, a)]:
                best = (state, action, self.actor.state_action_pairs[(state, a)])

        if random.random() < e_greedy or choose_best:
            m = best[1]
        else:
            m = random.choice(moves)
        return m

    def set_eligibility(self, state, action):
        self.actor.eligibility[(state, action.stringify())] = 1
        self.critic.eligibility[state] = 1
