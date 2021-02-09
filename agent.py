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
    def __init__(self, layers=4, sizes=[15, 8, 1]):
        super().__init__()
        self.model = torch.nn.Sequential()
        self.layers = []
        self.eligibility = [torch.zeros(param.shape) for param in self.parameters()]

        for i in range(len(sizes) - 1):
            layer = torch.nn.Linear(sizes[i], sizes[i + 1])
            self.model.add_module(f"{i}", layer)

    def forward(self, X):
        self.z = X
        for layer in self.model:
            self.z = layer(self.z)
            self.z = self.sigmoid(self.z)
        return self.z

    @staticmethod
    def sigmoid(s):
        return 1 / (1 + torch.exp(-s))

    @staticmethod
    def sigmoidPrime(s):
        # derivative of sigmoid
        return s * (1 - s)

    def backward(self, X, y, o):
        self.o_error = y - o  # error in output
        self.o_delta = self.o_error * self.sigmoidPrime(o)  # derivative of sig to error
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

            self.actor.eligibility[(state, action)] = self.cfg.discount * self.cfg.decay * self.actor.eligibility[
                (state, action)]

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
        self.critic.eligibility = [torch.zeros(param.shape) for param in self.critic.parameters()]
        self.episode = []

    def update(self, current_state, action, reward, new_state):
        self.episode.append((current_state, action.stringify()))
        print("Inne i UPDATE til NeuralAgent")
        self.set_eligibility(current_state, action)

        current_state_tensor = torch.Tensor([int(b) for b in current_state])
        new_state_tensor = torch.Tensor([int(b) for b in new_state])

        gamma = reward + self.cfg.discount * (self.critic(new_state_tensor) - self.critic(current_state_tensor))

        for (state, action) in self.episode:
            print("Inne i loopen til update")
            self.update_weights(state, gamma)

            # Update eligibility
            for i in range(len(self.critic.eligibility)):
                self.critic.eligibility[i] *= self.cfg.discount * self.cfg.decay

            self.actor.state_action_pairs[(state, action)] = self.actor.state_action_pairs[
                                                                 (state, action)] + self.cfg.learning_rate * gamma * \
                                                             self.actor.eligibility[(state, action)]

            self.actor.eligibility[(state, action)] = self.cfg.discount * self.cfg.decay * self.actor.eligibility[
                (state, action)]

    def update_weights(self, state, gamma):
        # Set gradients to zero
        self.critic.zero_grad()

        tensor_state = torch.Tensor([int(b) for b in state])
        pred_val = self.critic(tensor_state)
        pred_val.backward()
        # TODO: @wQuole look into logs

        for i, weight in enumerate(self.critic.parameters()):
            self.critic.eligibility[i] += weight.grad
            with torch.no_grad():
                print("self.critic.model[i]", self.critic.model[i])
                self.critic.model[i].weight.add_(self.cfg.learning_rate * gamma * self.critic.eligibility[i])

    def get_move(self, state, moves, e_greedy=0.3, choose_best=False):
        best = None

        for action in moves:
            print("Inne i get_move")
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
        self.critic.eligibility = [torch.ones(param.shape) for param in self.critic.parameters()]
