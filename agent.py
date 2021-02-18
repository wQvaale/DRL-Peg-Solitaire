import torch
import random
from collections import defaultdict


class Critic:

    def __init__(self):
        self.state_value = defaultdict(int)
        self.eligibility = defaultdict(int)


class NeuralCritic(torch.nn.Module):
    def __init__(self, dimensions):
        super().__init__()
        self.model = torch.nn.Sequential()
        self.relu = torch.nn.ReLU(inplace=True)
        self.eligibility = {name: 0 for name, w in self.named_parameters()}

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
        torch.save(model, "NN")


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

        td_error = reward + self.cfg.discount * self.critic.state_value[new_state] - self.critic.state_value[state]

        for (state, action) in self.episode:
            self.critic.state_value[state] += self.cfg.learning_rate * td_error * self.critic.eligibility[state]
            self.critic.eligibility[state] *= self.cfg.discount * self.cfg.decay

            self.actor.state_action_pairs[(state, action)] += self.cfg.learning_rate * td_error * self.actor.eligibility[(state, action)]
            self.actor.eligibility[(state, action)] *= self.cfg.discount * self.cfg.decay

    def get_move(self, state, moves, e_greedy):
        best = None

        for action in moves:
            a = action.stringify()
            candidate_action_value = self.actor.state_action_pairs[(state, a)]
            if best is None or best[1] < candidate_action_value:
                best = (action, candidate_action_value)

        if random.random() > e_greedy:
            m = best[0]
        else:
            m = random.choice(moves)
        return m

    def set_eligibility(self, state, action):
        self.actor.eligibility[(state, action.stringify())] = 1
        self.critic.eligibility[state] = 1


class NeuralAgent:
    def __init__(self, cfg):
        self.cfg = cfg
        self.critic = NeuralCritic(dimensions=self.cfg.layers)
        self.actor = Actor()
        self.episode = []
        self.wins = 0

    def flush(self):
        self.actor.eligibility = defaultdict(int)
        self.critic.eligibility = {name: 0 for name, w in self.critic.named_parameters()}
        self.episode = []

    def update(self, current_state, action, reward, new_state):
        self.episode.append((current_state, action.stringify()))
        self.set_eligibility(current_state, action)

        current_state_tensor = torch.Tensor([int(b) for b in current_state])
        new_state_tensor = torch.Tensor([int(b) for b in new_state])

        td_error = reward + self.cfg.discount * self.critic(new_state_tensor).item() - self.critic(current_state_tensor).item()

        for (state, action) in self.episode:
            self.update_weights(state, td_error)
            for name, weight in self.critic.named_parameters():
                self.critic.eligibility[name] *= self.cfg.discount * self.cfg.decay

            self.actor.state_action_pairs[(state, action)] += self.cfg.actor_learning_rate * td_error * self.actor.eligibility[(state, action)]
            self.actor.eligibility[(state, action)] = self.cfg.discount * self.cfg.decay * self.actor.eligibility[(state, action)]

    def update_weights(self, state, td_error):
        # Set gradients to zero
        self.critic.zero_grad()

        tensor_state = torch.Tensor([int(b) for b in state])
        pred_val = self.critic(tensor_state)
        pred_val.backward()

        for name, weight in self.critic.named_parameters():
            self.critic.eligibility[name] += weight.grad
            with torch.no_grad():
                weight.add_(self.cfg.learning_rate * td_error * self.critic.eligibility[name])

    def get_move(self, state, moves, e_greedy):
        best = None

        for action in moves:
            a = action.stringify()
            candidate_action_value = self.actor.state_action_pairs[(state, a)]
            if best is None or best[1] < candidate_action_value:
                best = (action, candidate_action_value)

        if random.random() > e_greedy:
            m = best[0]
        else:
            m = random.choice(moves)
        return m

    def set_eligibility(self, state, action):
        self.actor.eligibility[(state, action.stringify())] = 1
        self.critic.eligibility = {name: 1 for name, weights in self.critic.named_parameters()}
