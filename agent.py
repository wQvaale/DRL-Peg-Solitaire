import random
from config import Config
from collections import defaultdict


class RandomAgent:
    @staticmethod
    def get_move(moves):
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
