import torch
import random
from collections import defaultdict


class Critic:

    def __init__(self):
        self.state_value = defaultdict(int)
        self.eligibility = defaultdict(int)


class NeuralCritic(torch.nn.Module):
    def __init__(self, dimensions: list):
        super().__init__()
        self.model = torch.nn.Sequential()
        self.relu = torch.nn.ReLU(inplace=True)
        self.eligibility = {name: torch.zeros(w.shape) for name, w in self.named_parameters()}

        for i in range(len(dimensions) - 1):
            layer = torch.nn.Linear(dimensions[i], dimensions[i + 1])
            self.model.add_module(f"{i}", layer)

    def forward(self, data):
        x = data
        for layer in self.model:
            x = self.relu(layer(x))
        return x

    @staticmethod
    def sigmoid(s):
        return 1 / (1 + torch.exp(-s))

    @staticmethod
    def sigmoid_prime(s):
        # derivative of sigmoid
        return s * (1 - s)

    @staticmethod
    def save_weights(model):
        # we will use the PyTorch internal storage functions
        torch.save(model, "NN")
        # you can reload model with all the weights and so forth with:
        # torch.load("NN")


class Actor:

    def __init__(self):
        self.state_action_pairs = defaultdict(int)
        self.eligibility = defaultdict(int)


class TableAgent:
    def __init__(self, cfg):
        self.critic = Critic()
        self.actor = Actor()
        self.episode = []
        self.wins = 0
        self.cfg = cfg

    def flush(self):
        self.actor.eligibility = defaultdict(int)
        self.critic.eligibility = defaultdict(int)
        self.episode = []

    def update(self, state, action, reward, new_state):
        self.episode.append((state, action.stringify()))
        self.set_eligibility(state, action)
        # print("CriticValue:\t",self.critic.state_value)

        gamma = reward + self.cfg.discount * self.critic.state_value[new_state] - self.critic.state_value[state]

        for (state, action) in self.episode:
            self.critic.state_value[state] = self.critic.state_value[state] + self.cfg.learning_rate * gamma * \
                                             self.critic.eligibility[state]
            self.critic.eligibility[state] = self.cfg.discount * self.cfg.decay * self.critic.eligibility[state]
            self.actor.state_action_pairs[(state, action)] += self.cfg.learning_rate * gamma * self.actor.eligibility[(state, action)]

            self.actor.eligibility[(state, action)] = self.cfg.discount * self.cfg.decay * self.actor.eligibility[(state, action)]

    def get_move(self, state, moves, e_greedy=0.3, choose_best=False):
        best = None

        for action in moves:
            a = action.stringify()
            candidate_action_value = self.actor.state_action_pairs[(state, a)]
            if best is None or best[2] < candidate_action_value:
                best = (state, action, candidate_action_value)

        if random.random() > e_greedy or choose_best:
            m = best[1]
        else:
            m = random.choice(moves)
        return m

    def set_eligibility(self, state, action):
        self.actor.eligibility[(state, action.stringify())] = 1
        self.critic.eligibility[state] = 1


class NeuralAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        self.critic = NeuralCritic(dimensions=cfg.layers)
        self.actor = Actor()
        self.episode = []
        self.wins = 0

    def flush(self):
        self.actor.eligibility = defaultdict(int)
        self.critic.eligibility = {name: torch.zeros(w.shape) for name, w in self.critic.named_parameters()}
        self.episode = []

    def update(self, current_state, action, reward, new_state):
        self.episode.append((current_state, action.stringify()))
        self.set_eligibility(current_state, action)

        current_state_tensor = torch.Tensor([int(b) for b in current_state])
        new_state_tensor = torch.Tensor([int(b) for b in new_state])

        gamma = reward + self.cfg.discount * self.critic(new_state_tensor).item() - self.critic(current_state_tensor).item()

        for (state, action) in self.episode:
            self.update_weights(state, gamma)

            # Update eligibility
            for name, weight in self.critic.named_parameters():
                self.critic.eligibility[name] *= self.cfg.discount * self.cfg.decay

            self.actor.state_action_pairs[(state, action)] += self.cfg.learning_rate * gamma * self.actor.eligibility[(state, action)]

            self.actor.eligibility[(state, action)] = self.cfg.discount * self.cfg.decay * self.actor.eligibility[(state, action)]

    def update_weights(self, state, gamma):
        # Set gradients to zero
        self.critic.zero_grad()

        tensor_state = torch.Tensor([int(b) for b in state])
        pred_val = self.critic(tensor_state)
        pred_val.backward()

        for name, weight in self.critic.named_parameters():
            self.critic.eligibility[name] += weight.grad
            with torch.no_grad():
                weight.add_(self.cfg.learning_rate * gamma * self.critic.eligibility[name])

    def get_move(self, state, moves, e_greedy, choose_best=False):
        best = None

        for action in moves:
            a = action.stringify()
            candidate_action_value = self.actor.state_action_pairs[(state, a)]
            if best is None or best[2] < candidate_action_value:
                best = (state, action, candidate_action_value)

        if random.random() > e_greedy or choose_best:
            m = best[1]
        else:
            m = random.choice(moves)
        return m

    def set_eligibility(self, state, action):
        self.actor.eligibility[(state, action.stringify())] = 1
        self.critic.eligibility = {name: torch.ones(w.shape) for name, w in self.critic.named_parameters()}
